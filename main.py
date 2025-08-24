from fastapi import FastAPI, HTTPException
from kafka import KafkaProducer
import asyncio
import redis
import config

JOKES_DB = {
    1: "Why don't scientists trust atoms? Because they make up everything!",
    2: "I'm reading a book on anti-gravity. It's impossible to put down!",
    3: "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them."
}
app = FastAPI()
redis_client = redis.Redis(host = config.REDIS_HOST, port = config.REDIS_PORT, db = 0, decode_responses = True)
producer = KafkaProducer(bootstrap_servers = config.KAFKA_BROKER_URL,
                                   value_serializer = lambda v: str(v).encode("utf-8"))
@app.get("/joke")
async def joke():
    joke_key = "current_joke"
    cached_joke = redis_client.get(joke_key)

    if cached_joke:
        print("Serving from cache!")
        return {"joke": cached_joke}
    # ------- Cache Miss Logic ---------
    print("Cache miss. Generating new joke...")
    await asyncio.sleep(2)
    new_joke = "Why did the scarecrow win an award? Because he was outstanding in his field."

    # ------- Sending new joke to kafka --------
    print("Sending joke to Kafka...")
    producer.send(config.KAFKA_TOPIC_NAME, new_joke)
    producer.flush()

    # -------- Saving the cache to Redis --------
    redis_client.set(joke_key, new_joke, ex=10)
    return {"joke": new_joke}

@app.get("/joke/{joke_id}")
async def get_joke(joke_id: int):
    if joke_id in JOKES_DB:
        curr_joke = JOKES_DB[joke_id]
        return {"joke_id": joke_id, "joke": curr_joke}

    else:
        raise HTTPException(status_code = 404, detail = "Joke not found")
