from plot_twist_chatbot import PlotTwistChatbot

if __name__ == "__main__":
    # Create chatbot instance
    chatbot = PlotTwistChatbot()
    
    # Start the conversation
    chatbot.greeting()
    
    # Initial prompt
    response = chatbot.respond("Begin the adventure")
    
    # Main conversation loop
    while chatbot.conversation_is_active:
        try:
            response = chatbot.respond(response)
            
            # Check if user wants to quit
            user_input = chatbot.receive_input().lower()
            if user_input in ['quit', 'exit', 'goodbye', 'bye']:
                chatbot.conversation_is_active = False
            else:
                response = chatbot.respond(user_input)
                
        except KeyboardInterrupt:
            print("\n\nStory interrupted...")
            chatbot.conversation_is_active = False
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Let's continue the story...")
            response = "Please continue your adventure."
    
    # End conversation
    chatbot.farewell()