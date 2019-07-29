
import get_accountId
from get_contentInfo import get_contentId
from itemDetails import get_rootCategoryId
from accountIdPage import getAccountPage
from pybloom_live import ScalableBloomFilter




sdf = ScalableBloomFilter(initial_capacity=100, error_rate=0.001,
                          mode=ScalableBloomFilter.LARGE_SET_GROWTH)




def main():
    ids = [200114003706]

    contentId_total_list = []

    num = 1
    for id in ids :
        print(num)
        num += 1
        tags = get_accountId.get_tags(id)
        get_accountId.parse_tags(tags)

    for accountId_dict in get_accountId.accountInfo_list:

        contentId_obj = get_contentId(accountId_dict)
        contentId_obj.main()



    for accountId_dict in get_accountId.accountInfo_list:

        getAccountPage_obj = getAccountPage(accountId_dict.get('accountId'))
        contentId = getAccountPage_obj.get_allPage()

        if contentId not in sdf and contentId != '':
            contentId_total_list.append(contentId)
            sdf.add(contentId)




    while contentId_total_list:

        for contentId in contentId_total_list :
            tags = get_accountId.get_tags(contentId)
            get_accountId.parse_tags(tags)
            # 删除抓取过的contentId
            contentId_total_list.remove(contentId)


        for accountId_dict in get_accountId.accountInfo_list:
            contentId_obj = get_contentId(accountId_dict)
            contentId_obj.main()


        for accountId_dict in get_accountId.accountInfo_list:
            getAccountPage_obj = getAccountPage(accountId_dict.get('accountId'))
            contentId = getAccountPage_obj.get_allPage()

            if contentId not in sdf and contentId != '':
                contentId_total_list.append(contentId)
                sdf.add(contentId)

            # 删除抓取过的accountId
            get_accountId.accountInfo_list.remove(accountId_dict)






if __name__ == '__main__':
    main()