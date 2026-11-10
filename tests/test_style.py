import tempfile,unittest,json
from pathlib import Path
from creator_style_brain.__main__ import analyze_texts, profile_guide, draft_check, safe_text

class StyleTests(unittest.TestCase):
 def test_extract(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'mine.txt';p.write_text('我自己写的第一句。\n\n第二段怎么了？😂',encoding='utf-8')
   x=analyze_texts([p]);self.assertEqual(x['metrics']['file_count'],1)
   self.assertEqual(x['metrics']['paragraphs'],2)
   self.assertEqual(x['metrics']['question_marks'],1)
   self.assertIn('我自己写的',profile_guide(x))
 def test_check(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x.txt';p.write_text('这是样本。',encoding='utf-8')
   x=analyze_texts([p]);self.assertIn('赋能',draft_check(x,'这句话旨在赋能'))
 def test_too_large(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x.txt';p.write_bytes(b'a'*(2*1024*1024+1))
   with self.assertRaises(ValueError):safe_text(p)

if __name__=='__main__':unittest.main()
