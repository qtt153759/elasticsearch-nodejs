import sys
from pyvi.ViTokenizer import tokenize
import re

def preprocess(input_string):
    if not input_string :
      return ""



    def remove_html(txt):
        return re.sub(r'<[^>]*>', '', txt)
    
    # Chuẩn hóa unicode sang chuẩn unicode dựng sẵn
    def loaddicchar():
        dic = {}
        char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
            '|')
        charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
            '|')
        for i in range(len(char1252)):
            dic[char1252[i]] = charutf8[i]
        return dic


    dicchar = loaddicchar()


    def covert_unicode(txt):
        return re.sub(
            r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
            lambda x: dicchar[x.group()], str(txt))
    def standardize_data(row):
        # Xóa dấu chấm, phẩy, hỏi ở cuối câu
        row = re.sub(r"[\.,\?]+$-", "", row)

        # Xóa tất cả dấu chấm, phẩy, chấm phẩy, chấm thang, dấu gạch dưới ... trong câu
        row = row.replace(",", " ").replace(".", " ") \
            .replace(";", " ").replace("“", " ") \
            .replace(":", " ").replace("”", " ") \
            .replace('"', " ").replace("'", " ") \
            .replace("!", " ").replace("?", " ") \
            .replace("-", " ").replace("?", " ").replace("_", " ")
        
        # Xóa các kí tự đặc biệt
        row = re.sub("\W",' ', row) 

        # Xóa các đường link
        row = re.sub('https?://\S+|www\.\S+', ' ', row)

        # Xóa các số
        row = re.sub('\w*\d\w*', '', row)

        #Xóa các kí tự xuống dòng
        row = " ".join(re.sub("\n", " ", row).split())

        row = row.strip().lower()
        
        return row

    def remove_loop_char(text):
      text = re.sub(r'([A-Z])\1+', lambda m: m.group(1).upper(), str(text), flags=re.IGNORECASE)
      text = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]',' ',text)
      return text

    """**Tiền xử lý dữ liệu**"""
    # Làm sạch dữ liệu
    def text_prosessing(text):
        # Chuyển đổi thành chữ thường
        # text = text.lower() 

        # # Xóa các đoạn mã HTML
        # text = remove_html(text)

        # chuyển unicode tổ hợp sang chuẩn unicode dựng sẵn
        text = covert_unicode(text)

        # Thay thế từ viết tắt
        # text = replace_acronyms(text)

        # Xóa từ dừng
        # text = remove_stop_word(text)

        # Chuẩn hóa câu
        text = standardize_data(text)

        # Xử lý các từ viết trùng lắp
        text = remove_loop_char(text)

        # tách từ
        # text = sementation(text)

        return text
      
    clean_text=text_prosessing(input_string)
    tokenized_text=tokenize(clean_text)
    print(tokenized_text)
    return tokenized_text

if __name__ == "__main__":
    print(sys.argv[1])
    preprocess(sys.argv[1])