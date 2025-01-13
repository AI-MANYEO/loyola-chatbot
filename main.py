from app.utils.logger import setup_logger
import sys
import os
from app.modules.crawling import crawlLoggingTest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logger=setup_logger("main")
logger.info("Loyola Chatbot 초기화 중....")


if __name__ == "__main__":
    crawlLoggingTest()
    print("success")
    