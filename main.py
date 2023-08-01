from extraction import EmailFetcher
from support import AICustomerSupport
from dotenv import load_dotenv
import asyncio


async def fetch_and_process_emails(fetcher, ai_support):
    while True:
        print("Checking for new emails...")
        new_emails = await fetcher.fetch_new_emails()
        for email, sender_name, sender_addr in new_emails:
            extracted_properties, evaluation_result = await ai_support.process_email(email)
            print(f"Email from: {sender_name} ({sender_addr})")
            print(extracted_properties)
            print(evaluation_result)

            subject = "AI Customer Service Reply"
            fetcher.send_email(sender_addr, subject, evaluation_result)

        print("Sleeping for 10 seconds...")
        await asyncio.sleep(10)




async def main():
    load_dotenv()
    fetcher = EmailFetcher()
    ai_support = AICustomerSupport(openai_api_model="gpt-3.5-turbo")
    await fetch_and_process_emails(fetcher, ai_support)

if __name__ == "__main__":
    asyncio.run(main())
