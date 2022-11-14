if cam.data['instrusion']:
    fence = intr.fence()
    cv2.line(cam.frame, (fence.colist[0], fence.colist[1]), (fence.colist[2], fence.colist[3]),
             (255, 0, 0), 2)
    if 'person' in cam.e_list:
        trackers = multitracker.multitracker()
        fence.fence_check(cam.fxy_list, cam.frame)
        # 가상 펜스 침입
        if (fence.fence_warning):
            print("제한 구역 침입을 감지했습니다. 알림을 전송합니다.")
            if cam.data['instrusion'] == False:
                cam.data['cam_status'] = 'warning'
                cam.data['instrusion'] = True
                params = json.dumps(cam.data).encode("utf-8")
                req = urllib.request.Request(cam.url, data=params,
                                             headers={'content-type': 'application/json'})
                response = urllib.request.urlopen(req)
                print(response.read().decode('utf8'))
            fence.fence_warning = False
        else:
            print("해당 구역은 안전합니다.")
            if cam.data['instrusion'] == True:
                cam.data['cam_status'] = 'safe'
                cam.data['instrusion'] = False
                params = json.dumps(cam.data).encode("utf-8")
                req = urllib.request.Request(cam.url, data=params,
                                             headers={'content-type': 'application/json'})
                response = urllib.request.urlopen(req)
                print(response.read().decode('utf8'))

        # 사람이 처음 인식되었거나 사람 수가 변경되었을 때 객체 추적기 초기화
        if trackers.isFirst or trackers.peopleNum != len(cam.fxy_list):
            try:
                trackers.settings(cam.fxy_list, cam.frame)
                cam.count_tracking += 1
            except cv2.error as e:
                print(str(e))
                pass
        elif len(cam.fxy_list) != 0:  # 사람이 있을 때
            try:
                trackers.updatebox(cam.frame)
            except cv2.error as e:
                print(str(e))
                pass
        else:  # 사람이 감지되지 않았을 때
            trackers.isFirst = True
        # 월담 감지 시
        if trackers.warning == True:
            print("월담을 감지했습니다. 알림을 전송합니다.")
            if cam.data['instrusion'] == False:
                cam.data['cam_status'] = 'warning'
                cam.data['instrusion'] = True
                params = json.dumps(cam.data).encode("utf-8")
                req = urllib.request.Request(cam.url, data=params,
                                             headers={'content-type': 'application/json'})
                response = urllib.request.urlopen(req)
                print(response.read().decode('utf8'))
            trackers.warning = False
        else:
            print("해당 구역은 안전합니다.")
            if cam.data['instrusion'] == True:
                cam.data['cam_status'] = 'safe'
                cam.data['instrusion'] = False
                params = json.dumps(cam.data).encode("utf-8")
                req = urllib.request.Request(cam.url, data=params,
                                             headers={'content-type': 'application/json'})
                response = urllib.request.urlopen(req)
                print(response.read().decode('utf8'))
