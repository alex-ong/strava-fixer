from create_token.create_token import get_client

def main():
    client = get_client()
    activities = client.get_activities(limit=2)
    for activity in activities:
        print(activity)
        activity = client.get_activity(activity.id,include_all_efforts=True)
        print(activity)
    

if __name__ == "__main__":
    main()    
    