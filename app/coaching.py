import asyncio
from .profiler import generate_profile

async def stream_coaching_message(user_id):
    profile = generate_profile(user_id)
    pathology = ', '.join(profile['detectedPathologies'])
    sessions = ', '.join(profile['evidenceSessionIds'][:2])

    text = f"NevUp detected recurring {pathology}. Similar breakdown patterns appeared in sessions {sessions}. Slow position entry, cap risk after losses, and avoid emotionally reactive recovery trades."

    for word in text.split():
        yield word + " "
        await asyncio.sleep(0.08)