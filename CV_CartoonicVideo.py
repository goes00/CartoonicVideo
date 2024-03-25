import cv2

def cartoonize_video(input_file, output_file):
    # 입력 비디오 파일 열기
    cap = cv2.VideoCapture(input_file)
    
    # 비디오 출력 설정
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'XVID'), 60.0, (frame_width, frame_height))
    
    # 카툰화 효과를 적용할 함수 정의
    def apply_cartoon_effect(frame):
        # 그레이 스케일로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 중간값 블러 적용
        gray = cv2.medianBlur(gray, 5)
        
        # 가장자리 감지
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        
        # 카툰화 효과 적용
        color = cv2.bilateralFilter(frame, 9, 300, 300)
        cartoon = cv2.bitwise_and(color, color, mask=edges)
        
        return cartoon
    
    # 비디오 프레임 별로 카툰화 효과 적용
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 카툰화 효과 적용
        cartoon_frame = apply_cartoon_effect(frame)
        
        # 결과 비디오에 프레임 쓰기
        out.write(cartoon_frame)
        
        # 화면에 비디오 표시
        cv2.imshow('Cartoonized Video', cartoon_frame)
        
        # 종료 키
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 자원 해제
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# 입력 비디오 파일 경로 지정
input_file = 'input_video.mp4'

# 출력 비디오 파일 경로 지정
output_file = 'cartoonized_video.avi'

# 비디오 카툰화 함수 호출
cartoonize_video(input_file, output_file)