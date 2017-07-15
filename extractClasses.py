import json
import urllib.request
import time
import os.path

def findCourse(classList, className):
    for course in classList:
        courseName = course["className"]
        if courseName == className:
            return True
    return False

semesters = ["02016", "12016", "72016", "92016", "02017", "12017", "72017", "92017"]
#semesters = ["92017"]


for sems in semesters:
    print (sems)
    site = urllib.request.urlopen("https://sis.rutgers.edu/soc/subjects.json?semester=%s&campus=NB&level=U" %(sems))
    time.sleep(1)
    subjects = json.loads(site.read())

    #Setting up the subjects in the first row
    for subject in subjects:
        subName = subject["description"]
        subName=subName.replace("/",",")
        code = subject["code"]
        fullSubName = subName + " " + code
        if os.path.isfile("classData/"+fullSubName+".json"):
            classInfo = json.loads(open("classData/"+fullSubName+".json").read())
        else:
            classInfo = [{}, []]
            classInfo[0]["subject"] = fullSubName

        site2 = urllib.request.urlopen("http://sis.rutgers.edu/soc/courses.json?semester=%s&subject=%s&campus=NB&level=UG" %(sems, str(subject["code"])))
        time.sleep(1)
        classes = json.loads(site2.read())
        for course in classes:
            if course["expandedTitle"] is not None and not course["expandedTitle"].isspace():
                classList = classInfo[1]
                className = course["expandedTitle"]
                courseNum = course["courseNumber"]
                fullClassName = className+" "+courseNum
                fullClassName = " ".join(fullClassName.split())
                temp = course["coreCodes"]
                coreList = []
                for core in temp:
                    coreDes = core["description"]
                    code = core["code"]
                    coreList.append({"coreDescription": coreDes, "code": code})
                found = findCourse(classList, fullClassName)
                if found == False:
                    classList.append({"className": fullClassName, "coreStuff": coreList})
            else:
                classList = classInfo[1]
                className = course["title"]
                courseNum = course["courseNumber"]
                fullClassName = className+" "+courseNum
                fullClassName = " ".join(fullClassName.split())
                temp = course["coreCodes"]
                coreList = []
                for core in temp:
                    coreDes = core["description"]
                    code = core["code"]
                    coreList.append({"coreDescription": coreDes, "code": code})
                found = findCourse(classList, fullClassName)
                if found == False:
                    classList.append({"className": fullClassName, "coreStuff": coreList})

        with open('classData/'+fullSubName+'.json', 'w') as outfile:
                json.dump(classInfo, outfile)
                outfile.close()
        site2.close()
    site.close()



