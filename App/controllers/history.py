from flask import render_template
from app.models.User import *
from app.models.Result import *
import pandas as pd

def index():
    data = Result.join('users', 'users.id', '=', 'result.user_id')\
    .select('users.username', 'result.*')\
    .get().serialize()

    df = pd.DataFrame(data)
    if len(df) > 0:
        df = df.sort_values(by=['username'], ascending=True)
        df['created_at'] = df['created_at'].str.replace('T', ' ', regex=False)

    return render_template('pages/history.html', segment='history', df=df)
