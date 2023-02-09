# 🌠 Sixth Sense 팀의 Final 프로젝트


## 😎 Members
<table>
    <thead>
        <tr>
            <th>서장원</th>
            <th>박선규</th>
            <th>박세준</th>
            <th>장국빈</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td width="16%"><img src="https://user-images.githubusercontent.com/9074297/207550023-28ad4754-e60b-4a0c-835e-ea3c32108703.png" width="100%"/></td>
            <td width="16%"><img src="https://user-images.githubusercontent.com/9074297/207550543-a4a35f97-c647-4013-b440-dbfec61b01d7.png" width="100%"/></td>
            <td width="16%"><img src="https://user-images.githubusercontent.com/9074297/207550381-3f2deddb-ffef-4249-8738-66d27c83ea79.png" width="100%"/></td>
            <td width="16%"><img src="https://user-images.githubusercontent.com/9074297/207583484-e4cff046-7656-4c27-90c9-0ce116418e70.png" width="100%"/></td>
        </tr>
        <tr>
            <td align="center"><a href="https://github.com/nanpuhaha"><sub><sup>@nanpuhaha</sup></sub></a></td>
            <td align="center"><a href="https://github.com/Sungyu-Park"><sub><sup>@Sungyu-Park</sup></sub></a></td>
            <td align="center"><a href="https://github.com/sjleo1"><sub><sup>@sjleo1</sup></sub></a></td>
            <td align="center"><a href="https://github.com/JKbin"><sub><sup>@JKbin</sup></sub></a></td>
        </tr>
    </tbody>
</table>

## 🧑‍💻 Contributions

- 서장원 : Project Manager, Prepare Dataset, Service Develop, Experiments
- 박선규 : Experiments, Service Develop, Modeling
- 박세준 : Data Annotation, Experiments, Modeling, EDA
- 장국빈 : Data Pipeline, Data Cleaning, Experiments


## :car: Project Overview
<tr>
    <td width="16%"><img src="https://user-images.githubusercontent.com/71431029/217692076-d7a4a5bb-b5b5-4f5f-9d59-f50c9b1a1978.png" width="100%"/></td>
</tr>

여러분은 최근 우리나라에서 불거진 몇몇 구급차 길막 사건을 기억하고 계신가요?

이런 사건들은 사람의 의도적인 행동에서 비롯되었습니다. 하지만 자율주행 소프트웨어는 구급차와 소방차, 경찰차와 같은 긴급차량을 구분하지 못한다면 선택의 여지 없이 길을 비켜 주지 못할 것입니다.

자율주행 차량이 긴급차량을 위해 회피 경로를 탐색하고 차량을 제어하기 위해서는 긴급차량인지를 판단하는 과정이 먼저 이루어져야 하기 때문입니다.

따라서 저희는 자율주행 소프트웨어의 핵심적인 한 부분으로서 해당 주제를 선정하였습니다.

이뿐만 아니라 저희가 제작한 모델을 다른 분야에도 응용할 수 있습니다.

현재 전국적으로 긴급차량 우선신호 제어시스템이 확대 적용되고 있는 추세입니다. 긴급차량 우선신호 제어시스템이란 긴급차량의 요청에 따라 운영자가 신호 제어기를 조작해 우선신호를 받도록 하는 시스템입니다.

저희가 제작한 모델로 이러한 시스템을 자동화하여 훨씬 빠르고 안전하며 경제적으로 운용할 수 있을 것입니다.
<br>

## 💾 Dataset
1. [주행 차량 관점의 특수 차량 형상 데이터 (AIHub)](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=553)
2. [자율주행 및 ADAS AI인지모델 학습용 데이터 (AIHub)](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=461)

## 🧹 Data Cleaning
<img width="100%" src="https://user-images.githubusercontent.com/66928953/217619836-092502bc-6963-42f9-b1c3-597ba8aaa117.png"/>

확보 된 이미지 데이터의 일관성과 정확도를 위해 Data Cleaning 작업을 실시하였습니다.
결과 라벨링 오류 1,097건 / 육안으로 식별이 불가능 or 객체가 2/3 이상 가려져 있는 경우 1,324건 / 어노테이션 불량 371건이 발견되었습니다. 노이즈가 이는 이미지가 전체 이미지 대비 약 16%를 차지하여 라벨링 오류 및 식별 불가 이미지는 삭제 하고 어노테이션 불량 이미지는 재어노테이션 작업을 진행하였습니다.

## 🦾 Model

<table>
    <tr>
        <td width="16%"><img src="https://user-images.githubusercontent.com/66928953/217620261-5cf28935-5128-4625-9da5-9016404c9e59.png" width="100%"/></td>
        <td width="16%"><img src="https://user-images.githubusercontent.com/66928953/217620342-04dfc0d9-346c-468a-88df-938858cc2b3e.png" width="100%"/></td>
    </tr>
</table>

자율주행에 있어서 실시간으로 정확하게 객체를 탐지하는 것은 매우 중요합니다.
따라서 2-Stage Detector보다는 1-Stage Detector를 사용하는 것이 낫다고 판단했고, 이 중 빠르게 발전하고 있는 YOLO 모델을 사용하기로 결정하였습니다.

## 📃 Metric

<img width="100%" src="https://user-images.githubusercontent.com/66928953/217620478-112e3587-8de8-4a54-b13d-212b8aaecf20.png"/>

저희 팀은 모델별 성능을 비교하기 위해 정량적 지표와 정성적 지표를 도입하여 사용하였습니다.
정량적으로 평가하기 위해 클래스별 정확도를 평균내어 사용하는 mAP를 사용하였고, 정성적으로 평가하기 위해 팀 내부적으로 다섯 가지 지표를 고안하여 점수를 매긴 후 평균을 내는 방식을 사용하였습니다.

## ⚡ Service Develop

<img width="100%" src="https://user-images.githubusercontent.com/66928953/217620817-423da28d-bf37-4103-9c42-f776c7a91995.png"/>

- Streamlit : Frontend 제작
- FastAPI : Backend 제작
- Google Cloud SQL (MySQL):  이미지 데이터(업로드 시각, 원본 이미지 URL, 추론된 이미지 URL) 저장
- Google Cloud Storage : 원본 이미지 파일과 추론된 이미지 파일을 저장


## 📹Demo
<img width="90%" src="https://user-images.githubusercontent.com/66928953/217624520-21ad0631-a410-4b00-9622-3ea1dd279fbf.gif"/>

