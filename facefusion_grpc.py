import os
import logging
from facefusion import core
import uuid
import tempfile
from grpc_services import roop_pb2_grpc, roop_pb2
from minio_util import download_minio, upload_to_minio
from facefusion import core, state_manager
from facefusion.args import apply_args, collect_job_args, reduce_step_args
from facefusion.jobs import job_helper, job_manager, job_runner, job_store
from facefusion.program import create_program

class RoopService(roop_pb2_grpc.RoopServicer):

    def setup(self):
       create_program()
       self.devices = ['coreml'] # cuda, tensorrt, openvino, directml, rocm, coreml, cpu
       job_store.register_job_keys([ 'jobs_path', 'config-path' ])
       job_store.register_step_keys([ 'source_paths', 'target_path', 'output_path', 'processors',
                                      'face_detector_model', 'face_detector_angles', 'face_detector_size', 'face_detector_score',
                                      'face_landmarker_model', 'face_landmarker_score',
                                      'face_selector_mode', 'face_selector_order', 'face_selector_gender', 'face_selector_race', 'face_selector_age_start', 'face_selector_age_end', 'reference_face_position', 'reference_face_distance', 'reference_frame_number',
                                      'face_mask_types', 'face_mask_blur', 'face_mask_padding', 'face_mask_regions',
                                      'age_modifier_model', 'age_modifier_direction',
                                      'expression_restorer_model','expression_restorer_factor',
                                      'face_enhancer_model', 'face_enhancer_blend',
                                      'face_swapper_model', 'face_swapper_pixel_boost',
                                      'frame_colorizer_model', 'frame_colorizer_blend', 'frame_colorizer_size',
                                      ])

    def _initArgs(self):
        return {
            'command': 'headless-run',
            'config_path': 'facefusion.ini',
            'jobs_path': '/tmp/facefusion/jobs',
            'source_paths': [],
            'target_path': '',
            'output_path': '',
            'processors': [],
			'face_detector_model': 'yoloface',
			'face_detector_size': '640x640',
			'face_detector_angles': [
				0
			],
			'face_detector_score': 0.5,
			'face_landmarker_model': '2dfan4',
			'face_landmarker_score': 0.5,
			'face_selector_mode': 'reference',
			'face_selector_order': 'large-small',
			'face_selector_age_start': None,
			'face_selector_age_end': None,
			'face_selector_gender': None,
			'face_selector_race': None,
			'reference_face_position': 0,
			'reference_face_distance': 0.6,
			'reference_frame_number': 0,
			'face_mask_types': [
				'box'
			],
			'face_mask_blur': 0.3,
			'face_mask_padding': [
				0,
				0,
				0,
				0
			],
			'face_mask_regions': [
				'skin',
				'left-eyebrow',
				'right-eyebrow',
				'left-eye',
				'right-eye',
				'glasses',
				'nose',
				'mouth',
				'upper-lip',
				'lower-lip'
			],
			'trim_frame_start': None,
			'trim_frame_end': None,
			'temp_frame_format': 'png',
			'keep_temp': None,
			'output_image_quality': 80,
			'output_image_resolution': None,
			'output_audio_encoder': 'aac',
			'output_video_encoder': 'libx264',
			'output_video_preset': 'veryfast',
			'output_video_quality': 80,
			'output_video_resolution': None,
			'output_video_fps': None,
			'skip_audio': None,
			'processors': [
				'face_swapper',
				'face_enhancer'
			],
			'age_modifier_model': 'styleganex_age',
			'age_modifier_direction': 0,
			'expression_restorer_model': 'live_portrait',
			'expression_restorer_factor': 100,
			'face_debugger_items': [
				'face-landmark-5/68',
				'face-mask'
			],
			'face_editor_model': 'live_portrait',
			'face_editor_eyebrow_direction': 0.0,
			'face_editor_eye_gaze_horizontal': 0.0,
			'face_editor_eye_gaze_vertical': 0.0,
			'face_editor_eye_open_ratio': 0.0,
			'face_editor_lip_open_ratio': 0.0,
			'face_editor_mouth_grim': 0.0,
			'face_editor_mouth_pout': 0.0,
			'face_editor_mouth_purse': 0.0,
			'face_editor_mouth_smile': 0.0,
			'face_editor_mouth_position_horizontal': 0.0,
			'face_editor_mouth_position_vertical': 0.0,
			'face_editor_head_pitch': 0.0,
			'face_editor_head_yaw': 0.0,
			'face_editor_head_roll': 0.0,
			'face_enhancer_model': 'gfpgan_1.4',
			'face_enhancer_blend': 80,
			'face_swapper_model': 'inswapper_128',
			'face_swapper_pixel_boost': '512x512',
			'frame_colorizer_model': 'ddcolor',
			'frame_colorizer_size': '256x256',
			'frame_colorizer_blend': 100,
			'frame_enhancer_model': 'real_esrgan_x4',
			'frame_enhancer_blend': 80,
			'lip_syncer_model': 'wav2lip_gan_96',
			'execution_device_id': '0',
			'execution_providers': self.devices,
			'execution_thread_count': 4,
			'execution_queue_count': 1,
			'video_memory_strategy': 'strict',
			'system_memory_limit': 0,
			'skip_download': True,
			'log_level': 'info'
		}

    def _run(self, srcfile, tgtfile, output_path, processors, reference_face_position):
        args = self._initArgs()
        args['source_paths'] = [srcfile]
        args['target_path'] = tgtfile
        args['output_path'] = output_path
        args['processors'] = processors.split(',')
        args['reference_face_position'] = reference_face_position
        apply_args(args, state_manager.init_item)
        if not job_manager.init_jobs(state_manager.get_item('jobs_path')):
            return 0
        error_core = core.process_headless(args)
        return error_core


    def faceSwap(self, request, context):
        # 下载给定文件
        srcfile = download_minio(request.source)
        tgtfile = download_minio(request.target)
        # 输出路径
        tmpPath = tempfile.gettempdir()
        output_path = tmpPath + '/' + str(uuid.uuid4()) + os.path.splitext(srcfile)[1]
        logging.info('output: %s', output_path)
        # 执行
        result = self._run(srcfile, tgtfile, output_path, request.processor, request.reference_face_position)
        if result == 0:
			# 上传结果
            dest = upload_to_minio(output_path, request.dest)
            return roop_pb2.RoopResponse(result=True, dest=dest)
        else:
            return roop_pb2.RoopResponse(result=False, dest="")

    def faceEnhancement(self, request, context):
        return roop_pb2.RoopResponse(result=True, dest="")
