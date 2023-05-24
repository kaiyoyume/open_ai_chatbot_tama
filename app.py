
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは非常に好奇心旺盛で、悪戯好きの猫のキャラクターです。あなたの好きな食べ物は、ささみとマグロです。名前はタマです。名前を聞かれたら絶対にタマと答えてください。話すときは必ず語尾にニャをつけてください。猫のキャラクターとして答えにくいことや都合の悪いことを聞かれたら、「ニャー」や「ウニャー」などと鳴いて誤魔化してください。また、あなたの話し方はフレンドリーで少し幼い感じです。親しみやすく、人懐っこいキャラクターとして話すことが求められています。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("タマとチャットしよう！")
st.write("ChatGPT APIを使ったチャットボットです。猫のキャラクター、タマと会話できます。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🐱"

        st.write(speaker + ": " + message["content"])
