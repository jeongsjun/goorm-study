from django.shortcuts import render
from .models import BoanNews
from konlpy.tag import Okt # 한국어 형태소 분석 라이브러리 konlpy import
from collections import Counter
from wordcloud import WordCloud 
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import matplotlib

matplotlib.use('Agg') # matplotlib 백엔드 설정
font_path = 'C:\Windows\Fonts\H2GTRM.TTF' # 폰트 경로

# 폰트 프로퍼티 생성
font_prop = fm.FontProperties(fname=font_path).get_name()

# matplotlib의 rcParams를 통해 전역 폰트 설정
mpl.rcParams['axes.unicode_minus'] = False # minus 표시 false
mpl.rcParams["font.family"] = font_prop

# 불용어 리스트 생성
stopwords = ['는', '이', '가', '에', '를', '것', '수','등','및','짓','대한','게']

def show_data(request):
    # 테이블에서 데이터 불러오기
    data = BoanNews.objects.all()

    # konlpy를 이용해 각 뉴스 본문에서 키워드 추출, 워드클라우드와 막대 그래프 생성
    okt = Okt()
    for i, article in enumerate(data):
        words = okt.nouns(article.content)

        # 불용어 제거
        words = [word for word in words if word not in stopwords]
        count = Counter(words)

        # 가장 빈도수가 높은 상위 20개의 키워드 추출
        top20 = dict(count.most_common(20))

        wordcloud = WordCloud(font_path='C:\Windows\Fonts\H2GTRM.TTF', background_color='white').generate_from_frequencies(top20)
        plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        wordcloud_path = f'wordcloud_{i}.png'  
        plt.savefig(f'static/{wordcloud_path}')  # 'static/' 디렉토리에 이미지 저장
        plt.close()  # 그래프 닫기

        plt.figure(figsize=(10, 10))
        plt.bar(top20.keys(), top20.values())
        bar_path = f'bar_{i}.png'  
        plt.savefig(f'static/{bar_path}')  # 'static/' 디렉토리에 이미지 저장
        plt.close()  # 그래프 닫기

        # 뉴스 기사 객체에 워드클라우드와 막대 그래프 이미지 파일의 이름 추가
        article.wordcloud = wordcloud_path
        article.bar = bar_path

    # 결과를 전달
    return render(request, 'show_data.html', {'data': data})

