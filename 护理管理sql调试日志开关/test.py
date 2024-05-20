


sql = """
2024-05-14 17:31:04,722 DEBUG [admin-web] [DubboServerHandler-192.168.151.228:28181-thread-200] [c.b.i.d.Q.queryFocusedIssueReport_COUNT:143] -  ==>  Preparing: SELECT count(0) FROM (SELECT QD.STATISTICS_CONTENT_ID contentId, qd.STATISTICS_INDEX_ID processIndexId, qd.PROCESS_INDEX_NAME processIndexName, qd.CHECK_STANDARD_ID checkStandardId, qd.CHECK_STANDARD_NAME checkStandardName, qd.STANDARD_CATEGORY standardCategory, qd.DETAIL_ATTRIBUTES detailAttributes, qd.TARGET_ASSESSMENT_FLAG isTargetAssessment, COUNT(1) allTimes, sum(pat.patCount) patCount, COUNT(DECODE(decode(NVL(CONTENT_WEIGHT, 1), 0, 0, SCORE_RESULT / NVL(CONTENT_WEIGHT, 1)), 1, NULL, 1)) issueTimes, COUNT(DECODE(decode(NVL(CONTENT_WEIGHT, 1), 0, 0, SCORE_RESULT / NVL(CONTENT_WEIGHT, 1)), 1, NULL, 1)) / COUNT(1) issueRate, SUM(DECODE(SCORE_RESULT, -1, NULL, (decode(NVL(CONTENT_WEIGHT, 1), 0, 0, SCORE_RESULT / NVL(CONTENT_WEIGHT, 1)))) * FREQUENCY_NUM) / SUM(DECODE(SCORE_RESULT, -1, NULL, FREQUENCY_NUM)) averageScore FROM QC_PLAN_SCORE_RESULT_DETAIL QD JOIN QC_PLAN_SCORE_RESULT_BASE_INFO QI ON QD.SCORE_RESULT_BASE_INFO_ID = QI.ID LEFT JOIN QC_DATA_DICT DICT ON DICT.ID = QI.CONTENT_ID LEFT JOIN (SELECT count(1) AS patCount, BASE_ID FROM QC_PLAN_SCORE_RESULT_PAT_INFO p WHERE p.SCORE_RESULT_TYPE != 2 AND p.VALID_FLAG = 1 GROUP BY BASE_ID) pat ON pat.base_id = qi.id WHERE QD.VALID_FLAG = 1 AND qi.SCORE_RESULT_TYPE != 2 AND QI.VALID_FLAG = 1 AND QI.STATUS != 1 AND QI.SCORE_TIME BETWEEN ? AND ? AND (qd.SCORE_RESULT >= 0 OR qd.SCORE_RESULT IS NULL) AND QD.WARD_ID IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) GROUP BY QD.STATISTICS_CONTENT_ID, QD.STATISTICS_INDEX_ID, QD.PROCESS_INDEX_NAME, QD.CHECK_STANDARD_ID, QD.CHECK_STANDARD_NAME, QD.STANDARD_CATEGORY, QD.DETAIL_ATTRIBUTES, QD.TARGET_ASSESSMENT_FLAG) T WHERE issueTimes > 0
2024-05-14 17:31:04,723 DEBUG [admin-web] [DubboServerHandler-192.168.151.228:28181-thread-200] [c.b.i.d.Q.queryFocusedIssueReport_COUNT:143] -  ==> Parameters: 2024-05-01 00:00:00.0(Timestamp), 2024-05-31 23:59:59.0(Timestamp), d1d8e174a5d64d608fe9eb38eacb9fa9(String), de8bb3cb21174eea8cb69f7e9595ac58(String), 07b573fd962f417ca9018da363f726c1(String), 675aed6963a34854b43c80901ba1f6ae(String), 2ebc2bece00446378a8b0ff50f10b989(String), 45e48a448fe24c73b2786cfd5feb9408(String), 309b98a167204665829f84cfd25591c5(String), ef4ed50653784d0e894e9748df6c9719(String), fe08af3035694cc2bcf854fa3d1838c1(String), ad5ab1a68fa647db9453529ccf64b15d(String), f32d9a88e1df46b783feb78431790d66(String), 460cf73fbd6d43ebb4d6da7bb7bf6882(String), 8b24c7425a504784be6ad6bc02a469a8(String), aa58d6bf24e2442fa0091ae185e9e893(String), ab085e836d1a446483f46c4e1d816eef(String), 8ea2137e3fff4453beb9af4ac71921a9(String), e1bb763bfdf64988b7e6fbc34ab137af(String), f7b5a96fb357422884cf5643b69a162d(String), e4fb57dfe134472b86ba5c1d2d258bc8(String), cac32f914c3b49e8b95f43e4c9fe8b12(String), a426f5835b42430393dda07b535663e1(String), 774780807d164becaff4e3f1af5f7be3(String), c8e06a869652430d874ce29cd027f75b(String), 6938f000520f42a7975188d6049ae8fb(String), 127d5e5a8a274ee1aa9feb94b03c53b2(String), ffcfba8c27324282b7f254d50f97f333(String), 1ae68ba66a4846fda9bfbb4bc3f8f5e3(String), c8ae62687a1844c8a45592a37cb4bbd1(String), f68c20e61fc44a158d4331da1ac0088a(String), 746150a5fa0144508ba2479dadaaab1f(String), 5fe5814d18e946969c0cfa2c4748e92f(String), b4ebc9c32bba4553bc1aa3ed86fe78de(String), 43e235a4396540d981fbc7d9a66bd6ef(String), 632e396132af4120913ba39168210097(String), 1e1834c61a5a4ca389362c4c8a9f099f(String), 5d8cc82b82ba4c96b5685513ca8c57d0(String), 48599469be664d729534832923605eed(String), e832b91902ac43cb96e0942ce1b76d21(String), d3b3372b5e3145c0b3e5406d3cc6b209(String), 7512c83bcedc4bd7a2a78e244a37d31c(String), 55f5dbe3c5894036a7a9ac37768ec696(String), 7e295efdce564e668eb31b0095af3562(String), 3fbfcf74923c45558a2e46dcef134e2f(String), 8e91374c67f74825b83b0ce90c9bc615(String), 10fe7777877b4a98a1189a3d4eba47fe(String), 6fde8f00c50f4fec97b4398220d257b1(String), f4cfe268de99492195a19e271bad75e4(String), 46eb8190d1d44e4dab8df5cb760bb60c(String), 6e4da6af12bb44d990e1a0f33537e093(String), 98e8830528474447a6786d889dc4260d(String), a43b34df98b54aef9898c0c6101195e9(String), eaa851042cf343b69899273be98d8373(String), 70e4f6f8be27426ca879997e6ae3fb11(String), f9996f8a5e554d8094b8a14cbaadcf8a(String), beb0087e54354baa9305a4067bd4b14e(String), 61414ac6c37743829b10c6556483f3d1(String), 7e1b207b693e4c95a1bed707f399c2af(String), 5c23480481034416b30838d4c7c911d6(String), d595f30318c642f9bef7ce0c22cb85c7(String), 1aeed6ec1d7642a09267dd9fcdc8e7f3(String), efc1e2138e4a41c69d8fc5ef8bb655a2(String), 9230e39b59424c8ba5b11a2c0bb889e0(String), 39ff07cfcee842dc864ecc8943355d96(String), 3432c48311984cc197b29b5c123c809a(String), 0a2dc917a0734f1fa692030f869e22e1(String), ba92e13aed76430fb9c19e1a4ebef7b5(String), 0(String)
"""

def getParamByType(dbType, param):
    functions = {}
    result = {}
    with open("SourceCode.conf", "r") as f:
        sourceCode = f.read()
    try:
        exec(sourceCode, {}, functions)
    except Exception as e:
        print(e)
    try:
        exec(sourceCode, functions, result)
    except Exception as e:
        print(e)
    return result['getParamByType'](dbType, param)

def formatSql(dbType, sql):
    prepare = None
    params = None
    for row in sql.split("\n"):
        if "==>  Preparing: " in row:
            prepare = row.split("==>  Preparing: ")[1]
        if "==> Parameters: " in row:
            params = row.split("==> Parameters: ")[1]
    if prepare is None:
        return False, "sql语句为空，请检查！"
    if params is None:
        return False, "sql参数为空，请检查！"
    placeholders = prepare.count("?")
    paramsSize = params.count(",") + 1
    if placeholders == paramsSize:
        paramList = params.split(",")
        # 清除左右空格
        paramList = [p.strip() for p in paramList]
        # 反转列表以配合pop
        paramList.reverse()
        result = ""
        for str in prepare:
            if str == "?":
                result = result + getParamByType(dbType, paramList.pop())
            else:
                result = result + str
        return True, result
    else:
        return False, "sql语句与参数不匹配，请检查！"

if __name__ == "__main__":

    # print(formatSql("oracle", sql))
    ip = "xxx"
    port = "1902"
    headers = """{
  'Accept-Encoding'='gzip, deflate'
  'Accept-Language'='zh-CN,zh;q=0.9'
  'Cache-Control'='no-cache'
  'Origin'='http://{ip}:{port}'
  'Pragma'='no-cache'
  'Referer'='http://{ip}:{port}/nurse-admin-web/swagger-ui.html'
  'accept'='*/*'
} `""".format(ip=ip, port=port)
    print(headers)
