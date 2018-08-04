from urllib import request
import re
class Spider():
      #目标网站地址
      url = 'https://www.panda.tv/cate/lol'
      #包含目标信息的结构
      root_pattern = '<div class="video-info">([\s\S]*?)</div>'
      #主播昵称包含的位置
      name_pattern = '</i>([\s\S]*?)</span>'
      #该主播视频的访问量
      number_pattern = '<span class="video-number">([\s\S]*?)</span>'

      def __fetch_content(self):
          r = request.urlopen(Spider.url)
          htmls = r.read() #bytes
          htmls = str(htmls,encoding='utf-8')
          return htmls

      def __analysis(self, htmls):
          root_html = re.findall(Spider.root_pattern,htmls)

          anchors = []
          for html in root_html:
              name = re.findall(Spider.name_pattern,html)
              number = re.findall(Spider.number_pattern,html)
              anchor = {'name':name,'number':number}
              anchors.append(anchor)
          return anchors

      #数据精炼
      def __refine(self,anchors):
          l = lambda anchor:{'name':anchor['name'][0].strip(),
                             'number':anchor['number'][0]
                             }
          return map(l,anchors)

      #排序
      def __sort(self,anchors):
          anchors = sorted(anchors, key=self.__sort_seed,reverse=True)
          return anchors

      def __sort_seed(self,anchor):
          r = re.findall('\d*',anchor['number'])
          number = float(r[0])

          if '万' in anchor['number']:
              number *= 10000
          return  number

      #展现
      def __show(self,anchors):
          for rank in range(0,len(anchors)):
                  print("第" + str(rank+1)+ "名" + ": " + anchors[rank]["name"]+ "  " + anchors[rank]["number"] + "人")

      def go(self):
          htmls = self.__fetch_content()
          anchors = self.__analysis(htmls)
          anchors = list(self.__refine(anchors))
          anchors = self.__sort(anchors)
          self.__show(anchors)

spider = Spider()
spider.go()