import serial
import time
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
model="gpt-3.5-turbo",
base_url="https://api.avalai.ir/v1",
api_key="OPENAI_API_KEY"
)
ser = serial.Serial(port="COM4",  baudrate=115200, timeout=1,dsrdtr=False,rtscts=False)
ser.dtr = False
ser.rts=False

if not ser.is_open:
    ser.open()


def process_command(command):
    prompt = [
        {
            "role": "system",
            "content": """You are an assistant for an IoT system that
    controls LED lights. Based on the user's prompt, you must decide which
    function to call for controlling the lights.
    The function options are:
    A: turning on the light kitchen,
    B: turning off the light kitchen,
    C: turning on the light room,
    D: turning off the light room,
    E: turning on both kitchen and room lights,
    F: turning off both kitchen and room lights.
    G: turning on the light room and turning off the light kitchen,
    H: turning on the light kitchen and turning off the light room,.
    You must only respond with a single character (A, B, C, D, E, F, G or H)
    corresponding to the function. DO NOT add any other information or
    text.""",
        },
        {
            "role": "user",
            "content": command
        },
    ]
    response = llm.invoke(prompt)
    return response.content.strip()
try:
 print("hi")
 while True:
    if ser.in_waiting > 0:

      command = ser.readline().decode('utf-8').strip()
      if command.endswith('#'):
          response = process_command(command)
          ser.write(f"{response}\n".encode('utf-8'))
          print(f"Received command: {response}")
          print(ser.readline())
except KeyboardInterrupt:
 ser.close()

