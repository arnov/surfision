from fetch.cams import WijkCam, ScheveningCam, AnchorPointCam, SanSebastianCam, \
    SouthBeachCam, PettenCam


def get_cam(cam_id):
    if cam_id == 'wijk':
        cam = WijkCam()
    elif cam_id == 'scheveningen':
        cam = ScheveningCam()
    elif cam_id == 'anchorpoint':
        cam = AnchorPointCam()
    elif cam_id == 'sansebastian':
        cam = SanSebastianCam()
    elif cam_id == 'southbeach':
        cam = SouthBeachCam()
    elif cam_id == 'petten':
        cam = PettenCam()
    else:
        raise Exception(f'Cam not found: {cam_id}')

    return cam


def fetch_frame(cam_id='wijk'):
    cam = get_cam(cam_id)

    return cam.store_live_frame()


if __name__ == '__main__':
    fetch_frame()
