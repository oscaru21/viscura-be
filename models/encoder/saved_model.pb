
÷Ë
^
AssignVariableOp
resource
value"dtype"
dtypetype"
validate_shapebool( 

BiasAdd

value"T	
bias"T
output"T""
Ttype:
2	"-
data_formatstringNHWC:
NHWCNCHW
h
ConcatV2
values"T*N
axis"Tidx
output"T"
Nint(0"	
Ttype"
Tidxtype0:
2	
8
Const
output"dtype"
valuetensor"
dtypetype
$
DisableCopyOnRead
resource
Ž
GatherV2
params"Tparams
indices"Tindices
axis"Taxis
output"Tparams"

batch_dimsint "
Tparamstype"
Tindicestype:
2	"
Taxistype:
2	
.
Identity

input"T
output"T"	
Ttype
u
MatMul
a"T
b"T
product"T"
transpose_abool( "
transpose_bbool( "
Ttype:
2	

MergeV2Checkpoints
checkpoint_prefixes
destination_prefix"
delete_old_dirsbool("
allow_missing_filesbool( 

NoOp
M
Pack
values"T*N
output"T"
Nint(0"	
Ttype"
axisint 
C
Placeholder
output"dtype"
dtypetype"
shapeshape:

Prod

input"T
reduction_indices"Tidx
output"T"
	keep_dimsbool( ""
Ttype:
2	"
Tidxtype0:
2	
@
ReadVariableOp
resource
value"dtype"
dtypetype
E
Relu
features"T
activations"T"
Ttype:
2	
[
Reshape
tensor"T
shape"Tshape
output"T"	
Ttype"
Tshapetype0:
2	
o
	RestoreV2

prefix
tensor_names
shape_and_slices
tensors2dtypes"
dtypes
list(type)(0
l
SaveV2

prefix
tensor_names
shape_and_slices
tensors2dtypes"
dtypes
list(type)(0
?
Select
	condition

t"T
e"T
output"T"	
Ttype
d
Shape

input"T&
output"out_typeíout_type"	
Ttype"
out_typetype0:
2	
H
ShardedFilename
basename	
shard

num_shards
filename
Á
StatefulPartitionedCall
args2Tin
output2Tout"
Tin
list(type)("
Tout
list(type)("	
ffunc"
configstring "
config_protostring "
executor_typestring ¨
@
StaticRegexFullMatch	
input

output
"
patternstring
L

StringJoin
inputs*N

output"

Nint("
	separatorstring 
P
	Transpose
x"T
perm"Tperm
y"T"	
Ttype"
Tpermtype0:
2	
°
VarHandleOp
resource"
	containerstring "
shared_namestring "

debug_namestring "
dtypetype"
shapeshape"#
allowed_deviceslist(string)
 "serve*2.15.02v2.15.0-0-g6887368d6d48ŢĎ
ą
cnn__encoder/dense/biasVarHandleOp*
_output_shapes
: *(

debug_namecnn__encoder/dense/bias/*
dtype0*
shape:*(
shared_namecnn__encoder/dense/bias

+cnn__encoder/dense/bias/Read/ReadVariableOpReadVariableOpcnn__encoder/dense/bias*
_output_shapes	
:*
dtype0
ź
cnn__encoder/dense/kernelVarHandleOp*
_output_shapes
: **

debug_namecnn__encoder/dense/kernel/*
dtype0*
shape:
**
shared_namecnn__encoder/dense/kernel

-cnn__encoder/dense/kernel/Read/ReadVariableOpReadVariableOpcnn__encoder/dense/kernel* 
_output_shapes
:
*
dtype0

serving_default_input_1Placeholder*,
_output_shapes
:˙˙˙˙˙˙˙˙˙*
dtype0*!
shape:˙˙˙˙˙˙˙˙˙

StatefulPartitionedCallStatefulPartitionedCallserving_default_input_1cnn__encoder/dense/kernelcnn__encoder/dense/bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *,
_output_shapes
:˙˙˙˙˙˙˙˙˙*$
_read_only_resource_inputs
*F
config_proto64

CPU

GPU 

TPU


TPU_SYSTEM2J 8 *-
f(R&
$__inference_signature_wrapper_259404

NoOpNoOp
Ĺ
ConstConst"/device:CPU:0*
_output_shapes
: *
dtype0*
valueö
Bó
 Bě

Ĺ
	variables
trainable_variables
regularization_losses
	keras_api
__call__
*&call_and_return_all_conditional_losses
_default_save_signature
fc
	
signatures*


0
1*


0
1*
* 
°
non_trainable_variables

layers
metrics
layer_regularization_losses
layer_metrics
	variables
trainable_variables
regularization_losses
__call__
_default_save_signature
*&call_and_return_all_conditional_losses
&"call_and_return_conditional_losses*

trace_0* 

trace_0* 
* 
Ś
	variables
trainable_variables
regularization_losses
	keras_api
__call__
*&call_and_return_all_conditional_losses


kernel
bias*

serving_default* 
YS
VARIABLE_VALUEcnn__encoder/dense/kernel&variables/0/.ATTRIBUTES/VARIABLE_VALUE*
WQ
VARIABLE_VALUEcnn__encoder/dense/bias&variables/1/.ATTRIBUTES/VARIABLE_VALUE*
* 

0*
* 
* 
* 
* 
* 


0
1*


0
1*
* 

non_trainable_variables

layers
metrics
layer_regularization_losses
layer_metrics
	variables
trainable_variables
regularization_losses
__call__
*&call_and_return_all_conditional_losses
&"call_and_return_conditional_losses*

trace_0* 

 trace_0* 
* 
* 
* 
* 
* 
* 
* 
* 
O
saver_filenamePlaceholder*
_output_shapes
: *
dtype0*
shape: 
ę
StatefulPartitionedCall_1StatefulPartitionedCallsaver_filenamecnn__encoder/dense/kernelcnn__encoder/dense/biasConst*
Tin
2*
Tout
2*
_collective_manager_ids
 *
_output_shapes
: * 
_read_only_resource_inputs
 *F
config_proto64

CPU

GPU 

TPU


TPU_SYSTEM2J 8 *(
f#R!
__inference__traced_save_259477
ĺ
StatefulPartitionedCall_2StatefulPartitionedCallsaver_filenamecnn__encoder/dense/kernelcnn__encoder/dense/bias*
Tin
2*
Tout
2*
_collective_manager_ids
 *
_output_shapes
: * 
_read_only_resource_inputs
 *F
config_proto64

CPU

GPU 

TPU


TPU_SYSTEM2J 8 *+
f&R$
"__inference__traced_restore_259492Ă´
ů

$__inference_signature_wrapper_259404
input_1
unknown:

	unknown_0:	
identity˘StatefulPartitionedCallŐ
StatefulPartitionedCallStatefulPartitionedCallinput_1unknown	unknown_0*
Tin
2*
Tout
2*
_collective_manager_ids
 *,
_output_shapes
:˙˙˙˙˙˙˙˙˙*$
_read_only_resource_inputs
*F
config_proto64

CPU

GPU 

TPU


TPU_SYSTEM2J 8 **
f%R#
!__inference__wrapped_model_259336t
IdentityIdentity StatefulPartitionedCall:output:0^NoOp*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙<
NoOpNoOp^StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*/
_input_shapes
:˙˙˙˙˙˙˙˙˙: : 22
StatefulPartitionedCallStatefulPartitionedCall:U Q
,
_output_shapes
:˙˙˙˙˙˙˙˙˙
!
_user_specified_name	input_1:&"
 
_user_specified_name259398:&"
 
_user_specified_name259400

ű
A__inference_dense_layer_call_and_return_conditional_losses_259443

inputs5
!tensordot_readvariableop_resource:
.
biasadd_readvariableop_resource:	
identity˘BiasAdd/ReadVariableOp˘Tensordot/ReadVariableOp|
Tensordot/ReadVariableOpReadVariableOp!tensordot_readvariableop_resource* 
_output_shapes
:
*
dtype0X
Tensordot/axesConst*
_output_shapes
:*
dtype0*
valueB:_
Tensordot/freeConst*
_output_shapes
:*
dtype0*
valueB"       S
Tensordot/ShapeShapeinputs*
T0*
_output_shapes
::íĎY
Tensordot/GatherV2/axisConst*
_output_shapes
: *
dtype0*
value	B : ť
Tensordot/GatherV2GatherV2Tensordot/Shape:output:0Tensordot/free:output:0 Tensordot/GatherV2/axis:output:0*
Taxis0*
Tindices0*
Tparams0*
_output_shapes
:[
Tensordot/GatherV2_1/axisConst*
_output_shapes
: *
dtype0*
value	B : ż
Tensordot/GatherV2_1GatherV2Tensordot/Shape:output:0Tensordot/axes:output:0"Tensordot/GatherV2_1/axis:output:0*
Taxis0*
Tindices0*
Tparams0*
_output_shapes
:Y
Tensordot/ConstConst*
_output_shapes
:*
dtype0*
valueB: n
Tensordot/ProdProdTensordot/GatherV2:output:0Tensordot/Const:output:0*
T0*
_output_shapes
: [
Tensordot/Const_1Const*
_output_shapes
:*
dtype0*
valueB: t
Tensordot/Prod_1ProdTensordot/GatherV2_1:output:0Tensordot/Const_1:output:0*
T0*
_output_shapes
: W
Tensordot/concat/axisConst*
_output_shapes
: *
dtype0*
value	B : 
Tensordot/concatConcatV2Tensordot/free:output:0Tensordot/axes:output:0Tensordot/concat/axis:output:0*
N*
T0*
_output_shapes
:y
Tensordot/stackPackTensordot/Prod:output:0Tensordot/Prod_1:output:0*
N*
T0*
_output_shapes
:z
Tensordot/transpose	TransposeinputsTensordot/concat:output:0*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙
Tensordot/ReshapeReshapeTensordot/transpose:y:0Tensordot/stack:output:0*
T0*0
_output_shapes
:˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙
Tensordot/MatMulMatMulTensordot/Reshape:output:0 Tensordot/ReadVariableOp:value:0*
T0*(
_output_shapes
:˙˙˙˙˙˙˙˙˙\
Tensordot/Const_2Const*
_output_shapes
:*
dtype0*
valueB:Y
Tensordot/concat_1/axisConst*
_output_shapes
: *
dtype0*
value	B : §
Tensordot/concat_1ConcatV2Tensordot/GatherV2:output:0Tensordot/Const_2:output:0 Tensordot/concat_1/axis:output:0*
N*
T0*
_output_shapes
:
	TensordotReshapeTensordot/MatMul:product:0Tensordot/concat_1:output:0*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙s
BiasAdd/ReadVariableOpReadVariableOpbiasadd_readvariableop_resource*
_output_shapes	
:*
dtype0}
BiasAddBiasAddTensordot:output:0BiasAdd/ReadVariableOp:value:0*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙d
IdentityIdentityBiasAdd:output:0^NoOp*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙V
NoOpNoOp^BiasAdd/ReadVariableOp^Tensordot/ReadVariableOp*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*/
_input_shapes
:˙˙˙˙˙˙˙˙˙: : 20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp24
Tensordot/ReadVariableOpTensordot/ReadVariableOp:T P
,
_output_shapes
:˙˙˙˙˙˙˙˙˙
 
_user_specified_nameinputs:($
"
_user_specified_name
resource:($
"
_user_specified_name
resource

ű
A__inference_dense_layer_call_and_return_conditional_losses_259368

inputs5
!tensordot_readvariableop_resource:
.
biasadd_readvariableop_resource:	
identity˘BiasAdd/ReadVariableOp˘Tensordot/ReadVariableOp|
Tensordot/ReadVariableOpReadVariableOp!tensordot_readvariableop_resource* 
_output_shapes
:
*
dtype0X
Tensordot/axesConst*
_output_shapes
:*
dtype0*
valueB:_
Tensordot/freeConst*
_output_shapes
:*
dtype0*
valueB"       S
Tensordot/ShapeShapeinputs*
T0*
_output_shapes
::íĎY
Tensordot/GatherV2/axisConst*
_output_shapes
: *
dtype0*
value	B : ť
Tensordot/GatherV2GatherV2Tensordot/Shape:output:0Tensordot/free:output:0 Tensordot/GatherV2/axis:output:0*
Taxis0*
Tindices0*
Tparams0*
_output_shapes
:[
Tensordot/GatherV2_1/axisConst*
_output_shapes
: *
dtype0*
value	B : ż
Tensordot/GatherV2_1GatherV2Tensordot/Shape:output:0Tensordot/axes:output:0"Tensordot/GatherV2_1/axis:output:0*
Taxis0*
Tindices0*
Tparams0*
_output_shapes
:Y
Tensordot/ConstConst*
_output_shapes
:*
dtype0*
valueB: n
Tensordot/ProdProdTensordot/GatherV2:output:0Tensordot/Const:output:0*
T0*
_output_shapes
: [
Tensordot/Const_1Const*
_output_shapes
:*
dtype0*
valueB: t
Tensordot/Prod_1ProdTensordot/GatherV2_1:output:0Tensordot/Const_1:output:0*
T0*
_output_shapes
: W
Tensordot/concat/axisConst*
_output_shapes
: *
dtype0*
value	B : 
Tensordot/concatConcatV2Tensordot/free:output:0Tensordot/axes:output:0Tensordot/concat/axis:output:0*
N*
T0*
_output_shapes
:y
Tensordot/stackPackTensordot/Prod:output:0Tensordot/Prod_1:output:0*
N*
T0*
_output_shapes
:z
Tensordot/transpose	TransposeinputsTensordot/concat:output:0*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙
Tensordot/ReshapeReshapeTensordot/transpose:y:0Tensordot/stack:output:0*
T0*0
_output_shapes
:˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙
Tensordot/MatMulMatMulTensordot/Reshape:output:0 Tensordot/ReadVariableOp:value:0*
T0*(
_output_shapes
:˙˙˙˙˙˙˙˙˙\
Tensordot/Const_2Const*
_output_shapes
:*
dtype0*
valueB:Y
Tensordot/concat_1/axisConst*
_output_shapes
: *
dtype0*
value	B : §
Tensordot/concat_1ConcatV2Tensordot/GatherV2:output:0Tensordot/Const_2:output:0 Tensordot/concat_1/axis:output:0*
N*
T0*
_output_shapes
:
	TensordotReshapeTensordot/MatMul:product:0Tensordot/concat_1:output:0*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙s
BiasAdd/ReadVariableOpReadVariableOpbiasadd_readvariableop_resource*
_output_shapes	
:*
dtype0}
BiasAddBiasAddTensordot:output:0BiasAdd/ReadVariableOp:value:0*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙d
IdentityIdentityBiasAdd:output:0^NoOp*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙V
NoOpNoOp^BiasAdd/ReadVariableOp^Tensordot/ReadVariableOp*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*/
_input_shapes
:˙˙˙˙˙˙˙˙˙: : 20
BiasAdd/ReadVariableOpBiasAdd/ReadVariableOp24
Tensordot/ReadVariableOpTensordot/ReadVariableOp:T P
,
_output_shapes
:˙˙˙˙˙˙˙˙˙
 
_user_specified_nameinputs:($
"
_user_specified_name
resource:($
"
_user_specified_name
resource


&__inference_dense_layer_call_fn_259413

inputs
unknown:

	unknown_0:	
identity˘StatefulPartitionedCallô
StatefulPartitionedCallStatefulPartitionedCallinputsunknown	unknown_0*
Tin
2*
Tout
2*
_collective_manager_ids
 *,
_output_shapes
:˙˙˙˙˙˙˙˙˙*$
_read_only_resource_inputs
*F
config_proto64

CPU

GPU 

TPU


TPU_SYSTEM2J 8 *J
fERC
A__inference_dense_layer_call_and_return_conditional_losses_259368t
IdentityIdentity StatefulPartitionedCall:output:0^NoOp*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙<
NoOpNoOp^StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*/
_input_shapes
:˙˙˙˙˙˙˙˙˙: : 22
StatefulPartitionedCallStatefulPartitionedCall:T P
,
_output_shapes
:˙˙˙˙˙˙˙˙˙
 
_user_specified_nameinputs:&"
 
_user_specified_name259407:&"
 
_user_specified_name259409
˛'
¨
!__inference__wrapped_model_259336
input_1H
4cnn__encoder_dense_tensordot_readvariableop_resource:
A
2cnn__encoder_dense_biasadd_readvariableop_resource:	
identity˘)cnn__encoder/dense/BiasAdd/ReadVariableOp˘+cnn__encoder/dense/Tensordot/ReadVariableOp˘
+cnn__encoder/dense/Tensordot/ReadVariableOpReadVariableOp4cnn__encoder_dense_tensordot_readvariableop_resource* 
_output_shapes
:
*
dtype0k
!cnn__encoder/dense/Tensordot/axesConst*
_output_shapes
:*
dtype0*
valueB:r
!cnn__encoder/dense/Tensordot/freeConst*
_output_shapes
:*
dtype0*
valueB"       g
"cnn__encoder/dense/Tensordot/ShapeShapeinput_1*
T0*
_output_shapes
::íĎl
*cnn__encoder/dense/Tensordot/GatherV2/axisConst*
_output_shapes
: *
dtype0*
value	B : 
%cnn__encoder/dense/Tensordot/GatherV2GatherV2+cnn__encoder/dense/Tensordot/Shape:output:0*cnn__encoder/dense/Tensordot/free:output:03cnn__encoder/dense/Tensordot/GatherV2/axis:output:0*
Taxis0*
Tindices0*
Tparams0*
_output_shapes
:n
,cnn__encoder/dense/Tensordot/GatherV2_1/axisConst*
_output_shapes
: *
dtype0*
value	B : 
'cnn__encoder/dense/Tensordot/GatherV2_1GatherV2+cnn__encoder/dense/Tensordot/Shape:output:0*cnn__encoder/dense/Tensordot/axes:output:05cnn__encoder/dense/Tensordot/GatherV2_1/axis:output:0*
Taxis0*
Tindices0*
Tparams0*
_output_shapes
:l
"cnn__encoder/dense/Tensordot/ConstConst*
_output_shapes
:*
dtype0*
valueB: §
!cnn__encoder/dense/Tensordot/ProdProd.cnn__encoder/dense/Tensordot/GatherV2:output:0+cnn__encoder/dense/Tensordot/Const:output:0*
T0*
_output_shapes
: n
$cnn__encoder/dense/Tensordot/Const_1Const*
_output_shapes
:*
dtype0*
valueB: ­
#cnn__encoder/dense/Tensordot/Prod_1Prod0cnn__encoder/dense/Tensordot/GatherV2_1:output:0-cnn__encoder/dense/Tensordot/Const_1:output:0*
T0*
_output_shapes
: j
(cnn__encoder/dense/Tensordot/concat/axisConst*
_output_shapes
: *
dtype0*
value	B : č
#cnn__encoder/dense/Tensordot/concatConcatV2*cnn__encoder/dense/Tensordot/free:output:0*cnn__encoder/dense/Tensordot/axes:output:01cnn__encoder/dense/Tensordot/concat/axis:output:0*
N*
T0*
_output_shapes
:˛
"cnn__encoder/dense/Tensordot/stackPack*cnn__encoder/dense/Tensordot/Prod:output:0,cnn__encoder/dense/Tensordot/Prod_1:output:0*
N*
T0*
_output_shapes
:Ą
&cnn__encoder/dense/Tensordot/transpose	Transposeinput_1,cnn__encoder/dense/Tensordot/concat:output:0*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙Ă
$cnn__encoder/dense/Tensordot/ReshapeReshape*cnn__encoder/dense/Tensordot/transpose:y:0+cnn__encoder/dense/Tensordot/stack:output:0*
T0*0
_output_shapes
:˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙˙Ä
#cnn__encoder/dense/Tensordot/MatMulMatMul-cnn__encoder/dense/Tensordot/Reshape:output:03cnn__encoder/dense/Tensordot/ReadVariableOp:value:0*
T0*(
_output_shapes
:˙˙˙˙˙˙˙˙˙o
$cnn__encoder/dense/Tensordot/Const_2Const*
_output_shapes
:*
dtype0*
valueB:l
*cnn__encoder/dense/Tensordot/concat_1/axisConst*
_output_shapes
: *
dtype0*
value	B : ó
%cnn__encoder/dense/Tensordot/concat_1ConcatV2.cnn__encoder/dense/Tensordot/GatherV2:output:0-cnn__encoder/dense/Tensordot/Const_2:output:03cnn__encoder/dense/Tensordot/concat_1/axis:output:0*
N*
T0*
_output_shapes
:˝
cnn__encoder/dense/TensordotReshape-cnn__encoder/dense/Tensordot/MatMul:product:0.cnn__encoder/dense/Tensordot/concat_1:output:0*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙
)cnn__encoder/dense/BiasAdd/ReadVariableOpReadVariableOp2cnn__encoder_dense_biasadd_readvariableop_resource*
_output_shapes	
:*
dtype0ś
cnn__encoder/dense/BiasAddBiasAdd%cnn__encoder/dense/Tensordot:output:01cnn__encoder/dense/BiasAdd/ReadVariableOp:value:0*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙u
cnn__encoder/ReluRelu#cnn__encoder/dense/BiasAdd:output:0*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙s
IdentityIdentitycnn__encoder/Relu:activations:0^NoOp*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙|
NoOpNoOp*^cnn__encoder/dense/BiasAdd/ReadVariableOp,^cnn__encoder/dense/Tensordot/ReadVariableOp*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*/
_input_shapes
:˙˙˙˙˙˙˙˙˙: : 2V
)cnn__encoder/dense/BiasAdd/ReadVariableOp)cnn__encoder/dense/BiasAdd/ReadVariableOp2Z
+cnn__encoder/dense/Tensordot/ReadVariableOp+cnn__encoder/dense/Tensordot/ReadVariableOp:U Q
,
_output_shapes
:˙˙˙˙˙˙˙˙˙
!
_user_specified_name	input_1:($
"
_user_specified_name
resource:($
"
_user_specified_name
resource
  
Ő
__inference__traced_save_259477
file_prefixD
0read_disablecopyonread_cnn__encoder_dense_kernel:
?
0read_1_disablecopyonread_cnn__encoder_dense_bias:	
savev2_const

identity_5˘MergeV2Checkpoints˘Read/DisableCopyOnRead˘Read/ReadVariableOp˘Read_1/DisableCopyOnRead˘Read_1/ReadVariableOpw
StaticRegexFullMatchStaticRegexFullMatchfile_prefix"/device:CPU:**
_output_shapes
: *
pattern
^s3://.*Z
ConstConst"/device:CPU:**
_output_shapes
: *
dtype0*
valueB B.parta
Const_1Const"/device:CPU:**
_output_shapes
: *
dtype0*
valueB B
_temp/part
SelectSelectStaticRegexFullMatch:output:0Const:output:0Const_1:output:0"/device:CPU:**
T0*
_output_shapes
: f

StringJoin
StringJoinfile_prefixSelect:output:0"/device:CPU:**
N*
_output_shapes
: L

num_shardsConst*
_output_shapes
: *
dtype0*
value	B :f
ShardedFilename/shardConst"/device:CPU:0*
_output_shapes
: *
dtype0*
value	B : 
ShardedFilenameShardedFilenameStringJoin:output:0ShardedFilename/shard:output:0num_shards:output:0"/device:CPU:0*
_output_shapes
: 
Read/DisableCopyOnReadDisableCopyOnRead0read_disablecopyonread_cnn__encoder_dense_kernel"/device:CPU:0*
_output_shapes
 Ž
Read/ReadVariableOpReadVariableOp0read_disablecopyonread_cnn__encoder_dense_kernel^Read/DisableCopyOnRead"/device:CPU:0* 
_output_shapes
:
*
dtype0k
IdentityIdentityRead/ReadVariableOp:value:0"/device:CPU:0*
T0* 
_output_shapes
:
c

Identity_1IdentityIdentity:output:0"/device:CPU:0*
T0* 
_output_shapes
:

Read_1/DisableCopyOnReadDisableCopyOnRead0read_1_disablecopyonread_cnn__encoder_dense_bias"/device:CPU:0*
_output_shapes
 ­
Read_1/ReadVariableOpReadVariableOp0read_1_disablecopyonread_cnn__encoder_dense_bias^Read_1/DisableCopyOnRead"/device:CPU:0*
_output_shapes	
:*
dtype0j

Identity_2IdentityRead_1/ReadVariableOp:value:0"/device:CPU:0*
T0*
_output_shapes	
:`

Identity_3IdentityIdentity_2:output:0"/device:CPU:0*
T0*
_output_shapes	
:Ř
SaveV2/tensor_namesConst"/device:CPU:0*
_output_shapes
:*
dtype0*
valuexBvB&variables/0/.ATTRIBUTES/VARIABLE_VALUEB&variables/1/.ATTRIBUTES/VARIABLE_VALUEB_CHECKPOINTABLE_OBJECT_GRAPHs
SaveV2/shape_and_slicesConst"/device:CPU:0*
_output_shapes
:*
dtype0*
valueBB B B 
SaveV2SaveV2ShardedFilename:filename:0SaveV2/tensor_names:output:0 SaveV2/shape_and_slices:output:0Identity_1:output:0Identity_3:output:0savev2_const"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtypes
2
&MergeV2Checkpoints/checkpoint_prefixesPackShardedFilename:filename:0^SaveV2"/device:CPU:0*
N*
T0*
_output_shapes
:ł
MergeV2CheckpointsMergeV2Checkpoints/MergeV2Checkpoints/checkpoint_prefixes:output:0file_prefix"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 h

Identity_4Identityfile_prefix^MergeV2Checkpoints"/device:CPU:0*
T0*
_output_shapes
: S

Identity_5IdentityIdentity_4:output:0^NoOp*
T0*
_output_shapes
: 
NoOpNoOp^MergeV2Checkpoints^Read/DisableCopyOnRead^Read/ReadVariableOp^Read_1/DisableCopyOnRead^Read_1/ReadVariableOp*
_output_shapes
 "!

identity_5Identity_5:output:0*(
_construction_contextkEagerRuntime*
_input_shapes

: : : : 2(
MergeV2CheckpointsMergeV2Checkpoints20
Read/DisableCopyOnReadRead/DisableCopyOnRead2*
Read/ReadVariableOpRead/ReadVariableOp24
Read_1/DisableCopyOnReadRead_1/DisableCopyOnRead2.
Read_1/ReadVariableOpRead_1/ReadVariableOp:C ?

_output_shapes
: 
%
_user_specified_namefile_prefix:95
3
_user_specified_namecnn__encoder/dense/kernel:73
1
_user_specified_namecnn__encoder/dense/bias:=9

_output_shapes
: 

_user_specified_nameConst
Š

-__inference_cnn__encoder_layer_call_fn_259385
input_1
unknown:

	unknown_0:	
identity˘StatefulPartitionedCallü
StatefulPartitionedCallStatefulPartitionedCallinput_1unknown	unknown_0*
Tin
2*
Tout
2*
_collective_manager_ids
 *,
_output_shapes
:˙˙˙˙˙˙˙˙˙*$
_read_only_resource_inputs
*F
config_proto64

CPU

GPU 

TPU


TPU_SYSTEM2J 8 *Q
fLRJ
H__inference_cnn__encoder_layer_call_and_return_conditional_losses_259376t
IdentityIdentity StatefulPartitionedCall:output:0^NoOp*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙<
NoOpNoOp^StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*/
_input_shapes
:˙˙˙˙˙˙˙˙˙: : 22
StatefulPartitionedCallStatefulPartitionedCall:U Q
,
_output_shapes
:˙˙˙˙˙˙˙˙˙
!
_user_specified_name	input_1:&"
 
_user_specified_name259379:&"
 
_user_specified_name259381
Ş
ë
"__inference__traced_restore_259492
file_prefix>
*assignvariableop_cnn__encoder_dense_kernel:
9
*assignvariableop_1_cnn__encoder_dense_bias:	

identity_3˘AssignVariableOp˘AssignVariableOp_1Ű
RestoreV2/tensor_namesConst"/device:CPU:0*
_output_shapes
:*
dtype0*
valuexBvB&variables/0/.ATTRIBUTES/VARIABLE_VALUEB&variables/1/.ATTRIBUTES/VARIABLE_VALUEB_CHECKPOINTABLE_OBJECT_GRAPHv
RestoreV2/shape_and_slicesConst"/device:CPU:0*
_output_shapes
:*
dtype0*
valueBB B B ­
	RestoreV2	RestoreV2file_prefixRestoreV2/tensor_names:output:0#RestoreV2/shape_and_slices:output:0"/device:CPU:0* 
_output_shapes
:::*
dtypes
2[
IdentityIdentityRestoreV2:tensors:0"/device:CPU:0*
T0*
_output_shapes
:˝
AssignVariableOpAssignVariableOp*assignvariableop_cnn__encoder_dense_kernelIdentity:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0]

Identity_1IdentityRestoreV2:tensors:1"/device:CPU:0*
T0*
_output_shapes
:Á
AssignVariableOp_1AssignVariableOp*assignvariableop_1_cnn__encoder_dense_biasIdentity_1:output:0"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 *
dtype0Y
NoOpNoOp"/device:CPU:0*&
 _has_manual_control_dependencies(*
_output_shapes
 

Identity_2Identityfile_prefix^AssignVariableOp^AssignVariableOp_1^NoOp"/device:CPU:0*
T0*
_output_shapes
: U

Identity_3IdentityIdentity_2:output:0^NoOp_1*
T0*
_output_shapes
: L
NoOp_1NoOp^AssignVariableOp^AssignVariableOp_1*
_output_shapes
 "!

identity_3Identity_3:output:0*(
_construction_contextkEagerRuntime*
_input_shapes
: : : 2$
AssignVariableOpAssignVariableOp2(
AssignVariableOp_1AssignVariableOp_1:C ?

_output_shapes
: 
%
_user_specified_namefile_prefix:95
3
_user_specified_namecnn__encoder/dense/kernel:73
1
_user_specified_namecnn__encoder/dense/bias
Ę	
Ç
H__inference_cnn__encoder_layer_call_and_return_conditional_losses_259376
input_1 
dense_259369:

dense_259371:	
identity˘dense/StatefulPartitionedCall
dense/StatefulPartitionedCallStatefulPartitionedCallinput_1dense_259369dense_259371*
Tin
2*
Tout
2*
_collective_manager_ids
 *,
_output_shapes
:˙˙˙˙˙˙˙˙˙*$
_read_only_resource_inputs
*F
config_proto64

CPU

GPU 

TPU


TPU_SYSTEM2J 8 *J
fERC
A__inference_dense_layer_call_and_return_conditional_losses_259368k
ReluRelu&dense/StatefulPartitionedCall:output:0*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙f
IdentityIdentityRelu:activations:0^NoOp*
T0*,
_output_shapes
:˙˙˙˙˙˙˙˙˙B
NoOpNoOp^dense/StatefulPartitionedCall*
_output_shapes
 "
identityIdentity:output:0*(
_construction_contextkEagerRuntime*/
_input_shapes
:˙˙˙˙˙˙˙˙˙: : 2>
dense/StatefulPartitionedCalldense/StatefulPartitionedCall:U Q
,
_output_shapes
:˙˙˙˙˙˙˙˙˙
!
_user_specified_name	input_1:&"
 
_user_specified_name259369:&"
 
_user_specified_name259371"íL
saver_filename:0StatefulPartitionedCall_1:0StatefulPartitionedCall_28"
saved_model_main_op

NoOp*>
__saved_model_init_op%#
__saved_model_init_op

NoOp*ľ
serving_defaultĄ
@
input_15
serving_default_input_1:0˙˙˙˙˙˙˙˙˙A
output_15
StatefulPartitionedCall:0˙˙˙˙˙˙˙˙˙tensorflow/serving/predict:Í'
Ú
	variables
trainable_variables
regularization_losses
	keras_api
__call__
*&call_and_return_all_conditional_losses
_default_save_signature
fc
	
signatures"
_tf_keras_model
.

0
1"
trackable_list_wrapper
.

0
1"
trackable_list_wrapper
 "
trackable_list_wrapper
Ę
non_trainable_variables

layers
metrics
layer_regularization_losses
layer_metrics
	variables
trainable_variables
regularization_losses
__call__
_default_save_signature
*&call_and_return_all_conditional_losses
&"call_and_return_conditional_losses"
_generic_user_object
â
trace_02Ĺ
-__inference_cnn__encoder_layer_call_fn_259385
˛
FullArgSpec
args
jx
varargs
 
varkw
 
defaults
 

kwonlyargs 
kwonlydefaults
 
annotationsŞ *
 ztrace_0
ý
trace_02ŕ
H__inference_cnn__encoder_layer_call_and_return_conditional_losses_259376
˛
FullArgSpec
args
jx
varargs
 
varkw
 
defaults
 

kwonlyargs 
kwonlydefaults
 
annotationsŞ *
 ztrace_0
ĚBÉ
!__inference__wrapped_model_259336input_1"
˛
FullArgSpec
args

jargs_0
varargs
 
varkw
 
defaults
 

kwonlyargs 
kwonlydefaults
 
annotationsŞ *
 
ť
	variables
trainable_variables
regularization_losses
	keras_api
__call__
*&call_and_return_all_conditional_losses


kernel
bias"
_tf_keras_layer
,
serving_default"
signature_map
-:+
2cnn__encoder/dense/kernel
&:$2cnn__encoder/dense/bias
 "
trackable_list_wrapper
'
0"
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
ÓBĐ
-__inference_cnn__encoder_layer_call_fn_259385input_1"
˛
FullArgSpec
args
jx
varargs
 
varkw
 
defaults
 

kwonlyargs 
kwonlydefaults
 
annotationsŞ *
 
îBë
H__inference_cnn__encoder_layer_call_and_return_conditional_losses_259376input_1"
˛
FullArgSpec
args
jx
varargs
 
varkw
 
defaults
 

kwonlyargs 
kwonlydefaults
 
annotationsŞ *
 
.

0
1"
trackable_list_wrapper
.

0
1"
trackable_list_wrapper
 "
trackable_list_wrapper
­
non_trainable_variables

layers
metrics
layer_regularization_losses
layer_metrics
	variables
trainable_variables
regularization_losses
__call__
*&call_and_return_all_conditional_losses
&"call_and_return_conditional_losses"
_generic_user_object
ŕ
trace_02Ă
&__inference_dense_layer_call_fn_259413
˛
FullArgSpec
args

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs 
kwonlydefaults
 
annotationsŞ *
 ztrace_0
ű
 trace_02Ţ
A__inference_dense_layer_call_and_return_conditional_losses_259443
˛
FullArgSpec
args

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs 
kwonlydefaults
 
annotationsŞ *
 z trace_0
ĐBÍ
$__inference_signature_wrapper_259404input_1"
˛
FullArgSpec
args 
varargs
 
varkw
 
defaults
 

kwonlyargs
	jinput_1
kwonlydefaults
 
annotationsŞ *
 
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_list_wrapper
 "
trackable_dict_wrapper
ĐBÍ
&__inference_dense_layer_call_fn_259413inputs"
˛
FullArgSpec
args

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs 
kwonlydefaults
 
annotationsŞ *
 
ëBč
A__inference_dense_layer_call_and_return_conditional_losses_259443inputs"
˛
FullArgSpec
args

jinputs
varargs
 
varkw
 
defaults
 

kwonlyargs 
kwonlydefaults
 
annotationsŞ *
 
!__inference__wrapped_model_259336u
5˘2
+˘(
&#
input_1˙˙˙˙˙˙˙˙˙
Ş "8Ş5
3
output_1'$
output_1˙˙˙˙˙˙˙˙˙ş
H__inference_cnn__encoder_layer_call_and_return_conditional_losses_259376n
5˘2
+˘(
&#
input_1˙˙˙˙˙˙˙˙˙
Ş "1˘.
'$
tensor_0˙˙˙˙˙˙˙˙˙
 
-__inference_cnn__encoder_layer_call_fn_259385c
5˘2
+˘(
&#
input_1˙˙˙˙˙˙˙˙˙
Ş "&#
unknown˙˙˙˙˙˙˙˙˙˛
A__inference_dense_layer_call_and_return_conditional_losses_259443m
4˘1
*˘'
%"
inputs˙˙˙˙˙˙˙˙˙
Ş "1˘.
'$
tensor_0˙˙˙˙˙˙˙˙˙
 
&__inference_dense_layer_call_fn_259413b
4˘1
*˘'
%"
inputs˙˙˙˙˙˙˙˙˙
Ş "&#
unknown˙˙˙˙˙˙˙˙˙Š
$__inference_signature_wrapper_259404
@˘=
˘ 
6Ş3
1
input_1&#
input_1˙˙˙˙˙˙˙˙˙"8Ş5
3
output_1'$
output_1˙˙˙˙˙˙˙˙˙