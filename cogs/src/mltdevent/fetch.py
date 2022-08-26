async def GetNewest(session):
    async with session.get("https://api.matsurihi.me/mltd/v1/events") as response:
        try:
            data = await response.json()
            return data[-1]
        except Exception as e:
            print(f"exception occur: {e}")
            return {}
    
async def FetchBorder(evtid, session):
    async with session.get(f"https://api.matsurihi.me/mltd/v1/events/{evtid}/rankings/borderPoints") as response:
        try:
            data = await response.json()
            return data
        except Exception as e:
            print(f"exception occur: {e}")
            return {}