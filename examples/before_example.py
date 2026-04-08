# Dirty/Undocumented Code Example

# Unmaintainable function with multiple responsibilities
def process_user_data(data):
    users = []
    for d in data:
        if d['age'] >= 18:
            name = d['name'].strip().title()
            email = d['email'].lower()
            # Calculate score without reason
            score = (d['age'] - 18) * 0.5 + len(d['name']) * 0.1
            if score > 50:
                score = 50
            users.append({'name': name, 'email': email, 'score': score})
    return users

# Poorly structured class
class DataHandler:
    def __init__(self):
        self.data=[]
        self.filtered=[]
        self.processed=[]
    
    def add(self,item):
        self.data.append(item)
    
    def filter_adults(self):
        self.filtered=[x for x in self.data if x['age']>=18]
    
    def process_all(self):
        self.filter_adults()
        result=[]
        for user in self.filtered:
            user['name']=user['name'].strip().title()
            user['email']=user['email'].lower()
            result.append(user)
        self.processed=result
        
    def get_results(self):
        return self.processed

# Function with security issues
def save_user_info(user_id,info):
    import sqlite3
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    # Direct string interpolation - SQL injection vulnerability!
    query = f"INSERT INTO users VALUES({user_id},'{info}')"
    cur.execute(query)
    con.commit()
    con.close()
