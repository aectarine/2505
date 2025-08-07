* 세션 VS JWT/OAuth 선택 (!!중요!!)
  * 웹 페이지 구현 방식으로 구분하여 선택
✅ SPA (React, Vue, Svelte 등)
  * JWT + Refresh Token	API 호출 중심 구조에 적합. 토큰을 클라이언트에서 직접 관리
✅ 서버 렌더링 (Jinja2, HTMX, Django 템플릿 등)
  * 세션 기반 인증	쿠키 기반 인증이 자연스럽고 개발 간편. 서버가 사용자 상태 기억