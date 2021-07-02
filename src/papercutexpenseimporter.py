import os
import sys
import yaml
import smtpemailer as emailer
from datetime import datetime, timedelta
from customemail import customemail
from os import listdir

def main(*args):
    try:
        with open(".\\resources\\config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
            try:
                deleteInputFileAfterProcesing = cfg["delete_input_file_after_procesing"]
                email = customemail(cfg["email_recipient"], cfg["email_sender"], cfg["email_sender_pw"], "", "", "")
                inputFileLocation = cfg["input_file_location"]
                outputFileHistoryDays = cfg["output_file_history_days"]
                outputFilePath = cfg["output_file_path"]
                sendEmailOnError = cfg["send_email_on_error"]
                sendEmailOnSuccess = cfg["send_email_on_success"]
                timeKeeperInitial = cfg["time_keeper_intial"]
            except Exception as exception:
                raise Exception("Missing {} value from config.yml file!".format(str(exception)))

        importCount = importTxtFile(inputFileLocation, outputFilePath, timeKeeperInitial)
        cleanUpInputOutput(deleteInputFileAfterProcesing, inputFileLocation, outputFilePath, outputFileHistoryDays)
        if sendEmailOnSuccess:
            email.subject = "Succeded: PaperCut Expense Import!"
            email.message = "Successfully imported {} PaperCut prints into Cosmolex.".format(importCount)
            emailer.send_email(email)
    except Exception as exception:
        errorHandler(exception, email, sendEmailOnError)

def importTxtFile(inputFileLocation, outputFilePath, timeKeeperInitial):
    outputList = ""
    importCount = 0
    with open(inputFileLocation, "r") as inputFile:
        for inputData in inputFile:
            papercutData = inputData.split('|')
            oldFormatDate = papercutData[1]
            papercutDateSegments = oldFormatDate.split('/')
            date = datetime(int(papercutDateSegments[2]), int(papercutDateSegments[0]), int(papercutDateSegments[1]))
            papercutData[1] = date.strftime("%Y-%m-%d")
            papercutData.insert(2, timeKeeperInitial)
            outputList += '|'.join([x for x in papercutData])
            importCount += 1

    with open(getOutputFileLocation(outputFilePath), "w") as outputFile:
        outputFile.write(outputList)
    
    return importCount

def cleanUpInputOutput(deleteInputFileAfterProcesing, inputFileLocation, outputFilePath, outputFileHistoryDays):
    if deleteInputFileAfterProcesing and os.path.exists(inputFileLocation):
        os.remove(inputFileLocation)

    for outputFileName in listdir(outputFilePath):
        dateString = outputFileName.split("_")[0].split("-")
        fileDate = datetime(int(dateString[0]), int(dateString[1]), int(dateString[2]))
        deletionDate = datetime.now() - timedelta(outputFileHistoryDays)
        if deletionDate > fileDate:
            os.remove(outputFilePath + "\\" + outputFileName)
            
def getOutputFileLocation(outputFilePath):
    currentDate = datetime.now().strftime("%Y-%m-%d")
    return "{}\\{}_Cosmolex_PaperCut_Import.txt".format(outputFilePath, currentDate)

def errorHandler(exception, email, sendEmail):
    if sendEmail:
        email.subject = "Failed: PaperCut Expense Import!"
        email.message = str(exception)
        emailer.send_email(email)

    raise exception

# def log_error(errorMessage):
#     dateString = datetime.datetime.now().strftime("%Y-%m-%d")
#     errorLogFile = open('Backup Validator Logs\\{} Validator Error.log'.format(dateString), 'x')
#     errorLogFile.write(errorMessage)
