from fetch.cams import WijkCam, ScheveningCam


def fetch_frame(cam='wijk'):
    if cam == 'wijk':
        cam = WijkCam()
    elif cam == 'scheveningen':
        cam = ScheveningCam()
    else:
        raise Exception(f'Cam not found: {cam}')

    return cam.store_live_frame()


if __name__ == '__main__':
    fetch_frame()
