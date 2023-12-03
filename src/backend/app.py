import argparse
from distraction_modules.facemesh import Distraction


def main(save_video=None, v_cap=None):
    distract_detector = Distraction()
    distract_detector.distract_detection(v_cap=v_cap, save_video=save_video)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", "-s", required=False,
                        default=None, help="path to save video")
    parser.add_argument("--input", "-i", required=False, default=None,
                        help="path of input video, default is webcam")
    opt = parser.parse_args()

    main(opt.save, opt.input)
