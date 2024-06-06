import psycopg2
from psycopg2.extras import execute_values
from dataclasses import dataclass, field
from typing import Optional, List
import xml.etree.ElementTree as ET

from markdownify import markdownify as md


@dataclass
class Post:
    Id: int
    PostTypeId: int
    CreationDate: str
    Score: int
    Body: str
    OwnerUserId: int
    LastActivityDate: str
    ContentLicense: str
    ViewCount: Optional[int] = None
    AcceptedAnswerId: Optional[int] = None
    ParentId: Optional[int] = None
    DeletionDate: Optional[str] = None
    OwnerDisplayName: Optional[str] = None
    LastEditorUserId: Optional[int] = None
    LastEditorDisplayName: Optional[str] = None
    LastEditDate: Optional[str] = None
    Title: Optional[str] = None
    Tags: Optional[str] = None
    AnswerCount: Optional[int] = None
    CommentCount: Optional[int] = None
    FavoriteCount: Optional[int] = None
    ClosedDate: Optional[str] = None
    CommunityOwnedDate: Optional[str] = None

@dataclass
class Question(Post):
    answers: List[Post] = field(default_factory=list)

def parse_xml_to_dataclass(xml_data: str):
    root = ET.fromstring(xml_data)
    posts = []
    
    for row in root.findall('row'):
        post = Post(
            Id=int(row.attrib['Id']),
            PostTypeId=int(row.attrib['PostTypeId']),
            CreationDate=row.attrib['CreationDate'],
            Score=int(row.attrib['Score']),
            Body=md(row.attrib['Body']),
            OwnerUserId=int(row.attrib['OwnerUserId']) if 'OwnerUserId' in row.attrib else -1,
            LastActivityDate=row.attrib['LastActivityDate'],
            ContentLicense=row.attrib['ContentLicense'],
            ViewCount=int(row.attrib['ViewCount']) if 'ViewCount' in row.attrib else None,
            AcceptedAnswerId=int(row.attrib['AcceptedAnswerId']) if 'AcceptedAnswerId' in row.attrib else None,
            ParentId=int(row.attrib['ParentId']) if 'ParentId' in row.attrib else None,
            DeletionDate=row.attrib['DeletionDate'] if 'DeletionDate' in row.attrib else None,
            OwnerDisplayName=row.attrib['OwnerDisplayName'] if 'OwnerDisplayName' in row.attrib else None,
            LastEditorUserId=int(row.attrib['LastEditorUserId']) if 'LastEditorUserId' in row.attrib else None,
            LastEditorDisplayName=row.attrib['LastEditorDisplayName'] if 'LastEditorDisplayName' in row.attrib else None,
            LastEditDate=row.attrib['LastEditDate'] if 'LastEditDate' in row.attrib else None,
            Title=row.attrib['Title'] if 'Title' in row.attrib else None,
            Tags=row.attrib['Tags'] if 'Tags' in row.attrib else None,
            AnswerCount=int(row.attrib['AnswerCount']) if 'AnswerCount' in row.attrib else None,
            CommentCount=int(row.attrib['CommentCount']) if 'CommentCount' in row.attrib else None,
            FavoriteCount=int(row.attrib['FavoriteCount']) if 'FavoriteCount' in row.attrib else None,
            ClosedDate=row.attrib['ClosedDate'] if 'ClosedDate' in row.attrib else None,
            CommunityOwnedDate=row.attrib['CommunityOwnedDate'] if 'CommunityOwnedDate' in row.attrib else None,
        )
        posts.append(post)
    
    return posts

def organize_questions_and_answers(posts: List[Post]):
    questions = [Question(**post.__dict__) for post in posts if post.PostTypeId == 1]
    answers = [post for post in posts if post.PostTypeId == 2]

    for question in questions:
        question.answers = [answer for answer in answers if answer.ParentId == question.Id]

    return questions


def populate_posts_table(posts):
    # Connect to your postgres DB
    conn = psycopg2.connect("dbname=rags")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Prepare the data for insertion
    posts_data = [
        (
            post.Id, post.PostTypeId, post.CreationDate, post.Score, post.Body,
            post.OwnerUserId, post.LastActivityDate, post.ContentLicense, post.ViewCount,
            post.AcceptedAnswerId, post.ParentId, post.DeletionDate, post.OwnerDisplayName,
            post.LastEditorUserId, post.LastEditorDisplayName, post.LastEditDate, post.Title,
            post.Tags, post.AnswerCount, post.CommentCount, post.FavoriteCount,
            post.ClosedDate, post.CommunityOwnedDate
        )
        for post in posts
    ]

    # Insert data into the Post table
    insert_query = """
    INSERT INTO Post (
        Id, PostTypeId, CreationDate, Score, Body, OwnerUserId, LastActivityDate,
        ContentLicense, ViewCount, AcceptedAnswerId, ParentId, DeletionDate, OwnerDisplayName,
        LastEditorUserId, LastEditorDisplayName, LastEditDate, Title, Tags, AnswerCount,
        CommentCount, FavoriteCount, ClosedDate, CommunityOwnedDate
    ) VALUES %s
    ON CONFLICT (Id) DO NOTHING;
    """
    
    # Use execute_values to efficiently insert the data
    execute_values(cur, insert_query, posts_data)

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

if __name__ == '__main__':
    try:
        with open('data/Posts.xml', 'r') as f:
            xml_data = f.read()

        posts = parse_xml_to_dataclass(xml_data)
        questions = organize_questions_and_answers(posts)

        for question in questions:
            print(question)
            for answer in question.answers:
                print(f"  Answer: {answer}")
            break
        populate_posts_table(posts)

    except Exception as ex:
        import pdb; pdb.post_mortem()
        raise ex