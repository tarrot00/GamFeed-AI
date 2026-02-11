from github import Github, GithubException
import os
import streamlit as st
import datetime

def get_github_repo():
    token = os.getenv("GITHUB_TOKEN") or st.secrets.get("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO") or st.secrets.get("GITHUB_REPO")
    
    if not token or not repo_name:
        return None
    
    g = Github(token)
    return g.get_repo(repo_name)

def save_report_to_github(content):
    repo = get_github_repo()
    if not repo:
        return False, "GitHub 설정(Token/Repo)이 누락되었습니다."

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    month = datetime.datetime.now().strftime("%Y-%m")
    path = f"archives/{month}/{today}_daily_brief.md"
    
    message = f"docs: add daily brief for {today}"

    try:
        # 파일 존재 여부 확인
        try:
            contents = repo.get_contents(path)
            repo.update_file(contents.path, message, content, contents.sha)
            return True, f"✅ 기존 리포트 업데이트 완료 ({path})"
        except GithubException:
            repo.create_file(path, message, content)
            return True, f"✅ 새 리포트 저장 완료 ({path})"
            
    except Exception as e:
        return False, f"GitHub 저장 실패: {str(e)}"

def list_archived_reports():
    """아카이브 파일 목록 가져오기"""
    repo = get_github_repo()
    if not repo:
        return []
    
    reports = []
    try:
        # 최근 월 폴더 탐색 (현재 월)
        month = datetime.datetime.now().strftime("%Y-%m")
        contents = repo.get_contents(f"archives/{month}")
        for c in contents:
            if c.name.endswith(".md"):
                reports.append(c.path)
    except:
        pass # 폴더가 없으면 패스
    
    return sorted(reports, reverse=True)

def read_report(path):
    repo = get_github_repo()
    if not repo:
        return "GitHub 연결 실패"
    
    content = repo.get_contents(path)
    return content.decoded_content.decode("utf-8")
