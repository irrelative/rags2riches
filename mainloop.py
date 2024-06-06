


def main():
    while True:
        inp = input("History chat bot, how can I help you today?")

        # Ask LLM if input is a question about history
        # If yes, vectorize the input, and search against our pg vector db
            # Get match, use in LLM prompt to get response

        # Else, just send to LLM for response



if __name__ == '__main__':
    main()