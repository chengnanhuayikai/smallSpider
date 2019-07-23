# from details_content import details_content
from get_contentInfo import get_contentId







def main():

    wtdr_mixrow_num = 0
    wtdr_polymerization_num = 0
    wtdr_noLink_mixrow_num = 0
    wtdr_noLink_polymerization_num = 0


    accountId_f = open('accountId.txt','r')

    accountId_list = accountId_f.readlines()

    num = 1
    for accountId in accountId_list :


        contentId_obj = get_contentId(int(accountId.strip()))
        num_tuple = contentId_obj.main()
        wtdr_mixrow_num += num_tuple[0]
        wtdr_polymerization_num += num_tuple[1]
        wtdr_noLink_mixrow_num += num_tuple[2]
        wtdr_noLink_polymerization_num += num_tuple[3]
        break

    print('wt$polymerization:', wtdr_noLink_polymerization_num)
    print('wt$mixrow:', wtdr_noLink_mixrow_num)
    print('wt#polymerization:', wtdr_polymerization_num)
    print('wt#mixrow:', wtdr_mixrow_num)












    accountId_f.close()








if __name__ == '__main__':
    main()