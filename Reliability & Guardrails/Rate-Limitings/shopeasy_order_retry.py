import logging

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    before_sleep_log
)

logging.basicConfig(
    level=logging.INFO,
    filename="shopeas.log",
    filemode="w"
    
)

logger=logging.getLogger(__name__)

attempts_counter={"n":0}

@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1,min=1,max=10),
    before_sleep=before_sleep_log(logger,logging.WARNING)
)
def lookup_order_status(order_id: str) -> str:
    attempts_counter["n"] +=1
    if attempts_counter["n"]<=2:
         raise Exception("HTTP 429 Too Many Requests")
    return f"Order {order_id} — out for delivery. Expected by 6 PM today."

def main():
     print(lookup_order_status("1001"))
     print(attempts_counter["n"])

if __name__=="__main__":
     main()

     
     