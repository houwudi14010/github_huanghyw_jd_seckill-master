import threading
def my_job():
    print("111")






def func():
  # 每2s执行一次
  my_job()
  threading.Timer(2, func).start()


if __name__ == "__main__":
  a = {'x': 1}
  func()

