import argparse
import logging.config
import os
import warnings

import ReadVideo

warnings.filterwarnings('ignore')

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
log = logging.getLogger(__name__)

PATH_TO_VIDEO = 'video/'

def create_parser():
    parser = argparse.ArgumentParser(description='tutorial:')
    parser.add_argument('--video', '-v', dest='video', default='test.mp4', help='Videofile or stream url')
    parser.add_argument('--file', '-f', dest='filename', default='no', help='File with coordinates of plates')
    parser.add_argument('--type', '-t', dest='type', default='v', help='s-stream, v-videofile')
    parser.add_argument('--gpu', '-g', dest='gpu', default=False, help='If you use gpu write --gpu=True')
    parser.add_argument('--sec', '-s', dest='sec', default=0.5, help='Sec between process the cadrs')
    return parser


def parse_args(args):
    
    if args.gpu:
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'  # For GPU inference
        os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"  # For GPU inference
    else:
        os.environ['CUDA_VISIBLE_DEVICES'] = ''  # For CPU inference

    if args.type == 'v':
        name_of_video = os.path.splitext(args.video)[0]  # name of video without file extension
        path_video = PATH_TO_VIDEO + args.video
        if not os.path.exists(path_video):
            log.error(" %s didn't find" % path_video)
            exit(1)
    else:
        name_of_video = args.video
        path_video = args.video

    if args.filename == 'no':  # if name of file with txt doesn't point - it will be name of video
        filename = name_of_video + '.txt'
    else:
        filename = args.filename

    if args.sec == '0':
        sec = 0.1
    else:
        sec = float(args.sec)

    return PATH_VIDEO, filename, name_of_video, sec


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    path_video, filename, name_of_video = parse_args(args)

    log.info(' Run video %s' % args.video)
    ReadVideo.read_video(path_video, filename, args.type, name_of_video, float(args.sec))
    PATH_VIDEO, filename, name_of_video, sec = parse_args(args)

    log.info(' Run video %s' % args.video)
    ReadVideo.read_video(PATH_VIDEO, filename, args.type, name_of_video, sec)
    log.info(' Close video %s \n\n' % args.video)
