import pickle


class Direct(object):
  """docstring for Direct"""
  def __init__(self, dbfile):
    with open(dbfile, 'rb') as f:
      self.db = pickle.load(f)
    self.keyword_list = [k for k in self.db.keys()]
    self.keyword_list.sort()

  def search(self, query_range):
    p1 = self.keyword_list.index(query_range[0])
    p2 = self.keyword_list.index(query_range[-1])
    search_result = []
    for keyword in self.keyword_list[p1 : p2 + 1]:
      search_result.extend(self.db.get(keyword))
    return search_result