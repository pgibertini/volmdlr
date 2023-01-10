import dessia_common.workflow.core as wf
import dessia_common.workflow.blocks as blocks
import volmdlr as vm
from volmdlr import stl
from dessia_common.typings import MethodType

read_stl_method_type = blocks.ClassMethodType(class_=vm.stl.Stls, name='from_binary_streams')
cls_method_stl = blocks.ClassMethod(read_stl_method_type, name = 'STLFile')

to_volumemodel_method_type = blocks.MethodType(class_=vm.stl.Stls, name='to_volume_model')
method_volumemodel = blocks.ModelMethod(to_volumemodel_method_type, name = 'VolumeModel')


cadview_block = blocks.CadView(name='Display3D')

export_html = blocks.Export(method_type=MethodType(vm.core.VolumeModel, 'to_html_stream'), filename='VolumeModel.html', extension='html', text=True, name='Export_html')

pipes = [
         wf.Pipe(cls_method_stl.outputs[0], method_volumemodel.inputs[0]),

# Display and export definition
         wf.Pipe(method_volumemodel.outputs[0], cadview_block.inputs[0]),
         wf.Pipe(method_volumemodel.outputs[0], export_html.inputs[0]),
         ]


workflow_stl = wf.Workflow([cls_method_stl, method_volumemodel,
                            cadview_block,
                            export_html,
                            ],
                           pipes,
                           method_volumemodel.outputs[0],
                           name='From stl to volume model')

workflow_stl.description = "Import STL to Volume Model"

# workflow_stl.plot()


dict_workflow_stl = {i:j.name for i, j in enumerate(workflow_stl.inputs)}

# workflow_stl._check_platform()

# # =============================================================================
# # Usecase
# # =============================================================================
# from pathlib import Path

# from dessia_common.files import BinaryFile
# study_dir = str(Path('C:/Users/Mack/Documents/git/RenaultCustom/scripts/planche_de_bord/clean_translated_S49'))
# filename1 = 'CPOM0M4CFN_S52_traverse.stl'
# filename2 = 'CPOM0M4C6W_S52_planche.stl'

# with open(study_dir + '/Geometries_stl_files/'+filename1,'rb') as stream_1 ,\
#     open(study_dir + '/Geometries_stl_files/'+filename2,'rb') as stream_2:
    
#     str_file1 = BinaryFile(filename1)
#     str_file1.write(stream_1.read())
    
#     str_file2 = BinaryFile(filename2)
#     str_file2.write(stream_2.read())

#     input_values = {}
#     for i, j in dict_workflow_stl.items():
#         if 'streams' == j:
#             input_values[i] = [str_file1, str_file2]
#         elif 'filename' == j:
#             input_values[i] = filename1+'_'+filename2


#     workflow_run = workflow_stl.run(input_values)

# =============================================================================
# Platform insertion
# =============================================================================

# from dessia_api_client.users import PlatformUser
# platform = PlatformUser(api_url="https://api.renault.dessia.ovh")
# r = platform.objects.create_object_from_python_object(workflow_stl)