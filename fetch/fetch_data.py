from fetch.cams import WijkCam, ScheveningCam, AnchorPointCam, SanSebastianCam, \
    SouthBeachCam, PettenCam, WijkTimboektoeCam, MalibuCam, ZandvoortCam, \
    CastricumCam, ScheveningenHartBeachCam


ALL_CAMS = {'wijk': WijkCam(),
            'wijktim': WijkTimboektoeCam(),
            'scheveningen': ScheveningCam(),
            'anchorpoint': AnchorPointCam(),
            'sansebastian': SanSebastianCam(),
            'southbeach': SouthBeachCam(),
            'petten': PettenCam(),
            'malibu': MalibuCam(),
            'zandvoort': ZandvoortCam(),
            'castricum': CastricumCam(),
            'scheveningenhartbearch': ScheveningenHartBeachCam()}


def get_cam(cam_id):
    if cam_id not in ALL_CAMS:
        raise Exception(f'Cam not found: {cam_id}')

    return ALL_CAMS[cam_id]


def fetch_frame(cam_id='wijk'):
    cam = get_cam(cam_id)

    return cam.store_live_frame()


if __name__ == '__main__':
    fetch_frame()
