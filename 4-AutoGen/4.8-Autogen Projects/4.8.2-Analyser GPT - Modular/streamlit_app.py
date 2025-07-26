import os
import asyncio
import streamlit as st

from teams.analyzer_gpt import getDataAnalyzerTeam
from models.openai_model_client import get_model_client
from config.docker_util import getDockerCommandLineCodeExecutor, start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult


st.title('Analyser GPT- Digital Data Analyzer')

uploaded_file= st.file_uploader("upload a CSV file", type=["csv"])

task= st.chat_input("Enter your task here.....")

async def run_analyser_gpt(docker, openai_model_client, task):
    try:
        await start_docker_container(docker)
        team= getDataAnalyzerTeam(docker, openai_model_client)

        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                st.markdown(f"**{message.content}")
            elif isinstance(message, TaskResult):
                st.markdown(message.stop_reason)

        return None
    except Exception as ex:
        st.error(f"Error: {ex}")
        return ex

    finally:
        await stop_docker_container(docker)


if task:
    if uploaded_file is not None and task:
               
        if not os.path.exists('temp'):
            os.makedirs('temp', exist_ok=True)

        with open('temp/data.csv', 'wb') as fp:
            fp.write(uploaded_file.getbuffer())

        openai_model_client= get_model_client()
        docker= getDockerCommandLineCodeExecutor()

        error= asyncio.run(run_analyser_gpt(docker, openai_model_client, task))

        if error:
            st.error('An error occured', {error})

    else:
        st.warning("Please upload the file and provide the task")

else:
    st.warning('Please provide the task')