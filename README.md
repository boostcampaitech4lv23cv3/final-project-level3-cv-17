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

- 서장원 : Project Manager, Data Prepare, Service Develop
- 박선규 : Experiments, Service Develop, Modeling
- 박세준 : Data Annotation, Experiments, Modeling, EDA
- 장국빈 : Data Pipeline, Data Cleaning, Experiments


## :earth_asia: Project Overview
<table>
    <tr>
        <td width="16%"><img src="https://user-images.githubusercontent.com/66928953/217618626-aeb5a892-7f74-4c1f-9f00-5c069e6b289a.png" width="100%"/></td>
        <td width="16%"><img src="https://user-images.githubusercontent.com/66928953/217619086-668eb3bf-1d33-41c9-8442-171b678dde4d.png" width="100%"/></td>
    </tr>
</table>

생명을 구하는 골든타임이 화재 시 5분, 심정지 환자의 경우 4분이라고 합니다. 골든타임이 중요한 긴급차량 길 터주기는 선택이 아닌 의무입니다. [도로교통법 <제29조>긴급자동차의 우선 통행](https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EB%8F%84%EB%A1%9C%EA%B5%90%ED%86%B5%EB%B2%95/%EC%A0%9C29%EC%A1%B0)

  자율주행 자동차가 긴급 차량을 인식하지 못한다면 운전자의 개입이 불가피하므로 높은 자동화 레벨의 자율주행을 위해서는 긴급차량에 대한 대처가 필수적입니다. 주행 프로그램이 자동으로 긴급차량을 인식하여 긴급차량의 접근 시 길을 터주거나 운전자에게 알릴 수 있도록 도와주고자 이러한 주제를 선택하게 되었습니다. 또한, 현재 긴급차량 우선신호 제어시스템이 전국적으로 확대 시행되고 있습니다.

  긴급차량 우선신호 제어시스템이란 긴급차량의 요청이 있을 때 도시정보센터 내의 운영자가 관내 모든 신호 제어기를 조작해 우선신호를 받도록 하는 시스템입니다. 이러한 시스템을 딥러닝 방식으로 assist 하여 최적의 신호를 도출하고 출동 시간은 단축하고 출동 속도는 향상하여 피해를 최소화하는데 도움을 줄 것으로 기대됩니다.
<br>

## 💾 DataSet
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

