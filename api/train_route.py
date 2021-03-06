#Get information about all stations in the train's route
import json
import db

def getschedule(cdb,num):
    cdb._exec("SELECT * FROM schedule WHERE train=(?)",(num,))
    return cdb._fetchall()

def station_metadata(stn):
    with db.opendb(db.STNDB) as station:
        m=station.metadata(stn)
        return m
        
def format_result_json(m,s):
    d={}
    days=['SUN','MON','TUE','WED','THU','FRI','SAT']
    rundays=m['days']
    d['response_code']=200
    d['route']=[]
    d['train']=dict({'name':m['name']})
    d['train'].update({'number':m['number']})
    d['train'].update({'days':[]})
    for j in range(7):
        if days[j] in rundays:
            runs="Y"
        else:
            runs="N"
        d['train']['days'].append(dict({'day-code':days[j]}))
        d['train']['days'][j].update({"runs":runs})
    
    for i,val in enumerate(s):
        stn_md=station_metadata(val['station'])
        t={}
        t['no']=i+1
        t['scharr']=val['arrival']
        t['schdep']=val['departure']
        t['lat']=stn_md['lat']
        t['lng']=stn_md['lng']
        t['state']=stn_md['state']
        t['fullname']=stn_md['fullname']
        t['code']=stn_md['code']
        d['route'].append(t)

    d=json.dumps(d,indent=4)
    return d


def train_route(num):
    with db.opendb(db.TRAINDB) as train:
        m=train.metadata(num)
    with db.opendb(db.MAINDB) as train:
        s=getschedule(train,num)
    return format_result_json(m,s)

if __name__=="__main__":
    d=train_route("12555")
    print(d)
