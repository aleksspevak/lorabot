import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
import plotly.express as px
from .lorabot_sql import *
from PIL import Image, ImageDraw


class LoraBot:
    def __init__(self, bot_id):
        """
        LoraBot is a tool for complex analyze users, messages and events in chatbots.

        Parameters
        ----------
            bot_id: str
                the name of the bot that you specify in the code

        Returns
        -------
        LoraBot object.
        """
        load_dotenv()
        self.conn = psycopg2.connect(
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'))
        self.conn.autocommit = True
        self.sql = sql_queries
        self.check_db()
        self.conn.autocommit = True
        self.password = os.getenv('ANALYTICS_PASSWORD')
        self.bot_id = bot_id

    def check_db(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.sql['check_schema_and_tables'])
            value = cursor.fetchone()
            if value[0] != 4:
                cursor.execute(sql_ddl['create'])
            cursor.close()
        except Exception as error:
            print("There are some problems in check_db function: ", error)

    def check_password(self, password):
        """
        Compare entered password with password that set in ".env" file.

        Parameters
        ----------
            password: str
                entered password

        Returns
        -------
        Return True if password is correct and False if not.
        """
        if password == self.password:
            return True
        else:
            return False

    def _get_correct_database_query(self, query_name, add_date=False, message_type=None, event_type=None,
                                    events_for_funnel=None, messages_for_funnel=None):
        query = self.sql[query_name]
        if add_date:
            query = query.replace('''FROM lorabot.users WHERE bot_id = %(bot_id)s''',
                                  '''FROM lorabot.users WHERE bot_id = %(bot_id)s 
                                  and user_time between %(period_start)s and %(period_end)s''')
            query = query.replace('''FROM lorabot.messages WHERE bot_id = %(bot_id)s''',
                                  '''FROM lorabot.messages WHERE bot_id = %(bot_id)s 
                                  and message_time between %(period_start)s and %(period_end)s''')
            query = query.replace('''FROM lorabot.events WHERE bot_id = %(bot_id)s''',
                                  '''FROM lorabot.events WHERE bot_id = %(bot_id)s 
                                  and event_time between %(period_start)s and %(period_end)s''')
            query = query.replace('''FROM lorabot.bot_rating WHERE bot_id = %(bot_id)s''',
                                  '''FROM lorabot.bot_rating WHERE bot_id = %(bot_id)s 
                                  and rate_time between %(period_start)s and %(period_end)s''')
        if message_type is not None:
            query = query.replace('bot_id = %(bot_id)s', 'bot_id = %(bot_id)s and message_type = %(message_type)s ')
        if event_type is not None:
            query = query.replace('bot_id = %(bot_id)s', 'bot_id = %(bot_id)s and event_type = %(event_type)s ')
        if events_for_funnel is not None:
            query = query.replace('bot_id = %(bot_id)s',
                                  f'''bot_id = %(bot_id)s and event in ({"'" + "','".join(events_for_funnel) + "'"}) ''')
        if messages_for_funnel is not None:
            query = query.replace('bot_id = %(bot_id)s',
                                  f'''bot_id = %(bot_id)s and message in ({"'" + "','".join(messages_for_funnel) + "'"} )''')
        return query

    def user(self, user_id, language_code):
        """
        Insert new user to database.

        Parameters
        ----------
            user_id: str
                unique telegram user ID
            language_code: str
                user's language_code

        Returns
        -------
        Nothing.
        """
        try:
            cursor = self.conn.cursor()
            query = self._get_correct_database_query('user_check')
            cursor.execute(query, {'user_id': user_id, 'bot_id': self.bot_id})
            if cursor.fetchone() is None:
                query = self._get_correct_database_query('user_insert')
                cursor.execute(query, {'user_id': user_id, 'bot_id': self.bot_id, 'language_code': language_code})
            cursor.close()
        except Exception as error:
            print("There are some problems in user function: ", error)

    def message(self, message, message_type, user_id):
        """
        Insert new message to database.

        Parameters
        ----------
            message: str
                message from user
            message_type: str
                type of message from the user
            user_id: str
                unique telegram user ID

        Returns
        -------
        Nothing.
        """
        try:
            cursor = self.conn.cursor()
            query = self._get_correct_database_query('message')
            cursor.execute(query,
                           {'user_id': user_id, 'bot_id': self.bot_id, 'message': message,
                            'message_type': message_type})
            cursor.close()
        except Exception as error:
            print("There are some problems in message function: ", error)

    def event(self, event, event_type, user_id):
        """
        Insert new event to database.

        Parameters
        ----------
            event: str
                event from user
            event_type: str
                type of event from the user
            user_id: str
                unique telegram user ID

        Returns
        -------
        Nothing.
        """
        try:
            cursor = self.conn.cursor()
            query = self._get_correct_database_query('event')
            cursor.execute(query, {'user_id': user_id, 'bot_id': self.bot_id, 'event': event, 'event_type': event_type})
            cursor.close()
        except Exception as error:
            print("There are some problems in event function: ", error)

    def assessment(self, assessment, user_id):
        """
        Insert new assessment to database.

        Parameters
        ----------
            assessment: int
                assessment from user to bot
            user_id: str
                unique telegram user ID

        Returns
        -------
        Nothing.
        """
        try:
            cursor = self.conn.cursor()
            query = self._get_correct_database_query('assessment')
            cursor.execute(query, {'user_id': user_id, 'bot_id': self.bot_id, 'assessment': assessment})
            cursor.close()
        except Exception as error:
            print("There are some problems in assessment function: ", error)

    def review(self, review, user_id):
        """
        Insert new review to database.

        Parameters
        ----------
            review: int
                review from user to bot
            user_id: str
                unique telegram user ID

        Returns
        -------
        Nothing.
        """
        try:
            cursor = self.conn.cursor()
            query = self._get_correct_database_query('review')
            cursor.execute(query, {'user_id': user_id, 'bot_id': self.bot_id, 'review': review})
            cursor.close()
        except Exception as error:
            print("There are some problems in review function: ", error)

    def analyze_total(self, period_start=None, period_end=None):
        """
        Analyze total users, messages, events.

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Head metrics about chatbot.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_total', add_date)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = pd.DataFrame.from_records(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
            cursor.close()
            text = 'Total information:\n'
            for i in range(len(data)):
                text += f'{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return text
        except Exception as error:
            print("There are some problems in analyze_total function: ", error)
            return 'Error(maybe in varaibles)'

    def analyze_user_number_accumulation(self, period_start=None, period_end=None):
        """
        Analyze number of users with accumulation

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_user_number_accumulation', add_date)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            fig = px.bar(data, x=data['date'], y=data['amount'], title="Number of users with accumulation")
            photo = fig.to_image(format="png")
            cursor.close()
            text = 'Number of users with accumulation:\n'
            for i in range(len(data)):
                text += f'{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_user_number_accumulation function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_new_user(self, period_start=None, period_end=None):
        """
        Analyze number of new registered users

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_new_user', add_date)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            fig = px.bar(data, x=data['date'], y=data['amount'], title="New users")
            photo = fig.to_image(format="png")
            cursor.close()
            text = 'New users\n'
            for i in range(len(data)):
                text += f'{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_new_user function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_hour_activity(self, period_start=None, period_end=None):
        """
        Analyze number of message by hours activity

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_hour_activity', add_date)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            data['hour'] = data['hour'].astype(str)
            data = data.set_index('hour')
            fig = px.imshow(data, text_auto=True, aspect="auto", title="Hour Activity")
            photo = fig.to_image(format="png")
            cursor.close()
            return photo
        except Exception as error:
            print("There are some problems in analyze_hour_activity function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img

    def analyze_dau(self, period_start=None, period_end=None):
        """
        Analyze number of active users by days

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_dau', add_date)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            fig = px.bar(data, x=data['date'], y=data['amount'], title="Daily active users")
            photo = fig.to_image(format="png")
            cursor.close()
            text = 'Daily active users\n'
            for i in range(len(data)):
                text += f'{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_dau function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_wau(self, period_start=None, period_end=None):
        """
        Analyze number of active users by weeks

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_wau', add_date)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            fig = px.bar(data, x=data['date'], y=data['amount'], title="Weekly active users")
            photo = fig.to_image(format="png")
            cursor.close()
            text = 'Weekly active users\n'
            for i in range(len(data)):
                text += f'Week #{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_wau function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_mau(self, period_start=None, period_end=None):
        """
        Analyze number of active users by month

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_mau', add_date)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            fig = px.bar(data, x=data['date'], y=data['amount'], title="Monthly active users")
            photo = fig.to_image(format="png")
            cursor.close()
            text = 'Monthly active users\n'
            for i in range(len(data)):
                text += f'Month #{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_mau function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_yau(self, period_start=None, period_end=None):
        """
        Analyze number of active users by year

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_yau', add_date)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            fig = px.bar(data, x=data['date'], y=data['amount'], title="Yearly active users")
            photo = fig.to_image(format="png")
            cursor.close()
            text = 'Yearly active users\n'
            for i in range(len(data)):
                text += f'Year #{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_yau function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_messages_number(self, period_start=None, period_end=None, message_type=None):
        """
        Analyze number of messages by days

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period
            message_type: str
                type of message

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_messages_number', add_date, message_type=message_type)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start,
                                   'period_end': period_end, 'message_type': message_type})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            fig = px.bar(data, x=data['date'], y=data['amount'], title="Daily messages")
            photo = fig.to_image(format="png")
            cursor.close()
            if message_type is None:
                text = 'Daily messages\n'
            else:
                text = f'Daily messages with type {message_type}\n'
            for i in range(len(data)):
                text += f'{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_messages_number function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_messages(self, period_start=None, period_end=None, message_type=None, volume=100):
        """
        Analyze messages

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period
            message_type: str
                type of message
            volume:
                number of messages to show

        Returns
        -------
        Information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_messages', add_date, message_type=message_type)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start,
                                   'period_end': period_end, 'message_type': message_type})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            cursor.close()
            data = data[:volume]
            if message_type is None:
                text = 'Messages\n'
            else:
                text = f'Messages with type {message_type}\n'
            for i in range(len(data)):
                text += f'{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return text
        except Exception as error:
            print("There are some problems in analyze_messages function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_messages_type(self, period_start=None, period_end=None):
        """
        Analyze messages by types

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_messages_type', add_date)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            fig = px.pie(data, values='amount', names='type', title="Types of messages")
            photo = fig.to_image(format="png")
            cursor.close()
            text = f'Types of messages\n'
            for i in range(len(data)):
                text += f'{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_messages_type function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_messages_funnel(self, messages_for_funnel, period_start=None, period_end=None):
        """
        Create funnel for messages

        Parameters
        ----------
            messages_for_funnel: list of str
                array of messages in right order for funnel
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            if messages_for_funnel is None:
                return "You didn't set events for funnel"
            query = self._get_correct_database_query('analyze_messages_funnel', add_date,
                                                     messages_for_funnel=messages_for_funnel)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = cursor.fetchall()
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            sort_data = []
            message_funnel = []
            for message_for_position in messages_for_funnel:
                for values in data:
                    if message_for_position == values[0]:
                        message_funnel.append(values[0])
                        sort_data.append(values[1])
            data = dict(
                number=sort_data,
                message=message_funnel)
            fig = px.funnel(data, x='number', y='message', title='Funnel of messages')
            photo = fig.to_image(format="png")
            cursor.close()
            text = f'Funnel of messages\n'
            for message, number in zip(message_funnel, sort_data):
                text += f'{message} {number}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_messages_funnel function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_events_number(self, period_start=None, period_end=None, event_type=None):
        """
        Analyze number of events by days

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period
            event_type: str
                type of event

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_events_number', add_date, event_type=event_type)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start,
                                   'period_end': period_end, 'event_type': event_type})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            fig = px.bar(data, x=data['date'], y=data['amount'], title="Daily events with type")
            photo = fig.to_image(format="png")
            cursor.close()
            if event_type is None:
                text = 'Daily events\n'
            else:
                text = f'Daily events with type {event_type}\n'
            for i in range(len(data)):
                text += f'{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_events_number function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_events(self, period_start=None, period_end=None, event_type=None, volume=100):
        """
        Analyze events

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period
            event_type: str
                type of events
            volume:
                number of messages to show

        Returns
        -------
        Information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_events', add_date, event_type=event_type)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start,
                                   'period_end': period_end, 'event_type': event_type})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            data = data[:volume]
            cursor.close()
            if event_type is None:
                text = 'Events\n'
            else:
                text = f'Events with type {event_type}\n'
            for i in range(len(data)):
                text += f'{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return text
        except Exception as error:
            print("There are some problems in analyze_events function: ", error)
            return 'Error(maybe in varaibles)'

    def analyze_events_type(self, period_start=None, period_end=None):
        """
        Analyze events by types

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_events_type', add_date)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            fig = px.pie(data, values='amount', names='type', title='Types of events')
            photo = fig.to_image(format="png")
            cursor.close()
            text = f'Types of events\n'
            for i in range(len(data)):
                text += f'{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_events_type function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_events_funnel(self, events_for_funnel=None, period_start=None, period_end=None):
        """
        Create funnel for events

        Parameters
        ----------
            events_for_funnel: list of str
                array of events in right order for funnel
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            if events_for_funnel is None:
                return "You didn't set events for funnel"
            query = self._get_correct_database_query('analyze_events_funnel', add_date,
                                                     events_for_funnel=events_for_funnel)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = cursor.fetchall()
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            sort_data = []
            event_funnel = []
            for event_for_position in events_for_funnel:
                for values in data:
                    if event_for_position == values[0]:
                        event_funnel.append(values[0])
                        sort_data.append(values[1])
            data = dict(
                number=sort_data,
                event=event_funnel)
            fig = px.funnel(data, x='number', y='event', title='Funnel of events')
            photo = fig.to_image(format="png")
            cursor.close()
            text = f'Funnel of events\n'
            for event, number in zip(event_funnel, sort_data):
                text += f'{event} {number}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_events_funnel function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_assessment(self, period_start=None, period_end=None):
        """
        Analyze assessment

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_assessment', add_date)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            fig = px.pie(data, values='amount', names='assessment', title='Assessment')
            photo = fig.to_image(format="png")
            cursor.close()
            text = f'Assessment\n'
            for i in range(len(data)):
                text += f'Rate {data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_assessment function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_review(self, period_start=None, period_end=None, volume=5):
        """
        Analyze review

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period
            volume:
                number of review to show

        Returns
        -------
        Information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_review', add_date)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start, 'period_end': period_end})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            cursor.close()
            text = f'Review\n'
            data = data[:volume]
            for i in range(len(data)):
                text += f'#{i+1} {data.iloc[i, 0]}\n'
            return text
        except Exception as error:
            print("There are some problems in analyze_review function: ", error)
            return 'Error(maybe in varaibles)'

    def analyze_language(self, period_start=None, period_end=None):
        """
        Analyze what language users use

        Parameters
        ----------
            period_start: str
                beginning of the analysis period
            period_end: str
                end of the analysis period

        Returns
        -------
        Photo in bytes format and information in string format.
        """
        try:
            cursor = self.conn.cursor()
            if period_start is not None and period_end is not None:
                add_date = True
            else:
                add_date = False
            query = self._get_correct_database_query('analyze_language', add_date)
            cursor.execute(query, {'bot_id': self.bot_id, 'period_start': period_start,'period_end': period_end})
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            if len(data) == 0:
                img = Image.new('RGB', (100, 100))
                d = ImageDraw.Draw(img)
                d.text((40, 45), "Nothing")
                return img, 'No data'
            fig = px.pie(data, values='amount', names='type', title='Language')
            photo = fig.to_image(format="png")
            cursor.close()
            text = 'Language\n'
            for i in range(len(data)):
                text += f'{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return photo, text
        except Exception as error:
            print("There are some problems in analyze_language function: ", error)
            img = Image.new('RGB', (100, 100))
            d = ImageDraw.Draw(img)
            d.text((40, 45), "Error")
            return img, 'Error(maybe in varaibles)'

    def analyze_bots_users(self):
        """
        Analyze number of users in all bots

        Returns
        -------
        Information in string format.
        """
        try:
            cursor = self.conn.cursor()
            query = self._get_correct_database_query('analyze_bots_users')
            cursor.execute(query)
            data = pd.DataFrame.from_records(cursor.fetchall(),
                                             columns=[desc[0] for desc in cursor.description])
            text = "Bot's users\n"
            for i in range(len(data)):
                text += f'{data.iloc[i, 0]} {data.iloc[i, 1]}\n'
            return text
        except Exception as error:
            print("There are some problems in analyze_bots_users function: ", error)
            return 'Error'

    def sql_query(self, query):
        """
        Run SQL queries in database.

        Parameters
        ----------
            query: str
                query for analysis

        Returns
        -------
        Information in string format.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            text = 'Answer:\n'
            text = text + "   ".join(columns) + "\n"
            for i in data:
                row = ''
                for j in i:
                    row += f'{str(j)}   '
                text += f"{row}\n"
            cursor.close()
            return text
        except Exception as error:
            print("There are some problems in sql function: ", error)
