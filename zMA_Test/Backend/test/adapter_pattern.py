class Adapter:

    def getList(self, final_dict):
        final_list = []
        for w2 in final_dict:
            final_list.append([w2['wordID'], w2['word'], w2['meaning'], w2['usage'], w2['translations'], w2['TYPE']])
        return final_list




