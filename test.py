import ffpb
from tqdm import tqdm
import sys

ffpb.main(argv=["-i", "https://vidroxy.com/eyJhbGciOiJIUzI1NiJ9.eyJzcnYiOjIxLCJkIjoxLCJuIjoianVqdXRzdS1rYWlzZW4iLCJzIjoiMSIsImUiOiIyMiIsInEiOiIxMDgwIn0.s0sBOFj_T5zVdCHsbVHe4OEDy5U_ZnV6qNRJgTc2DHk.m3u8", "test.mp4"], stream=sys.stderr, encoding=None, tqdm=tqdm)

