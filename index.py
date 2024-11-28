from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)
CORS(app)  


file_path = 'data.xlsx'  # Ensure this path is correct
df = pd.read_excel(file_path)

df.rename(columns={
    'SERVICE NUMBER AND BRANCH': 'Branch',
    'appointment unit': 'AppointmentUnit',
    'COMMISSIONED': 'Commissioned',
    'STREAM': 'Stream',
    'PROMOTIONS GAZETTED': 'PromotionsGazetted',
    'Training and other courses': 'TrainingCourses',
    'BADGES QULIFIED': 'BadgesQualified',
    'AWARDS': 'Awards',
    'IMAGES': 'Images',
    'RETIRED ON': 'RetiredOn'
}, inplace=True)

df['Branch'] = df['Branch'].astype(str)
df['AppointmentUnit'] = df['AppointmentUnit'].astype(str)
df['Stream'] = df['Stream'].astype(str)
df['TrainingCourses'] = df['TrainingCourses'].astype(str)
df['BadgesQualified'] = df['BadgesQualified'].astype(str)
df['Awards'] = df['Awards'].astype(str)

df['PromotionsGazetted'] = df['PromotionsGazetted'].apply(lambda x: len(str(x).split('\n')))

label_encoder_branch = LabelEncoder()
label_encoder_appointment_unit = LabelEncoder()
label_encoder_stream = LabelEncoder()
label_encoder_training_courses = LabelEncoder()
label_encoder_badges_qualified = LabelEncoder()
label_encoder_awards = LabelEncoder()

df['Branch'] = label_encoder_branch.fit_transform(df['Branch'])
df['AppointmentUnit'] = label_encoder_appointment_unit.fit_transform(df['AppointmentUnit'])
df['Stream'] = label_encoder_stream.fit_transform(df['Stream'])
df['TrainingCourses'] = label_encoder_training_courses.fit_transform(df['TrainingCourses'])
df['BadgesQualified'] = label_encoder_badges_qualified.fit_transform(df['BadgesQualified'])
df['Awards'] = label_encoder_awards.fit_transform(df['Awards'])

X = df[['Branch', 'Stream', 'PromotionsGazetted', 'TrainingCourses', 'BadgesQualified', 'Awards']]
y = df['AppointmentUnit']

model = DecisionTreeClassifier()
model.fit(X, y)

def recommend_posting(officer_data):
    officer_df = pd.DataFrame([officer_data])
    officer_df['Branch'] = officer_df['Branch'].map(lambda x: label_encoder_branch.transform([x])[0] if x in label_encoder_branch.classes_ else -1)
    officer_df['Stream'] = officer_df['Stream'].map(lambda x: label_encoder_stream.transform([x])[0] if x in label_encoder_stream.classes_ else -1)
    officer_df['TrainingCourses'] = officer_df['TrainingCourses'].map(lambda x: label_encoder_training_courses.transform([x])[0] if x in label_encoder_training_courses.classes_ else -1)
    officer_df['BadgesQualified'] = officer_df['BadgesQualified'].map(lambda x: label_encoder_badges_qualified.transform([x])[0] if x in label_encoder_badges_qualified.classes_ else -1)
    officer_df['Awards'] = officer_df['Awards'].map(lambda x: label_encoder_awards.transform([x])[0] if x in label_encoder_awards.classes_ else -1)
    prediction = model.predict(officer_df[['Branch', 'Stream', 'PromotionsGazetted', 'TrainingCourses', 'BadgesQualified', 'Awards']])
    return label_encoder_appointment_unit.inverse_transform(prediction)[0]

@app.route('/recommend_posting', methods=['POST'])
def recommend_posting_endpoint():
    data = request.json
    recommended_posting = recommend_posting(data)
    return jsonify({'recommended_posting': recommended_posting})

if __name__ == '__main__':
    app.run(debug=True)
