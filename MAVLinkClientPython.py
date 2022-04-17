from __future__ import print_function
from vicon_dssdk import ViconDataStream
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('host', nargs='?', 
                    help="Host name, in the format of server:port", 
                    default = "localhost:801")
args = parser.parse_args()

client = ViconDataStream.Client()

while True:

    print('NEW POSITION')

    try:
        client.Connect( args.host )

        # Check setting the buffer size works
        client.SetBufferSize( 1 )

        #Enable all the data types
        client.EnableSegmentData()
        client.EnableMarkerData()
        client.EnableUnlabeledMarkerData()
        client.EnableMarkerRayData()
        client.EnableDeviceData()
        client.EnableCentroidData()

        HasFrame = False
        while not HasFrame:
            try:
                client.GetFrame()
                HasFrame = True
            except ViconDataStream.DataStreamException as e:
                client.GetFrame()
        
        # Try setting the different stream modes
        client.SetStreamMode( ViconDataStream.Client.StreamMode.EClientPull )
        print( 'Get Frame Pull', client.GetFrame(), client.GetFrameNumber() )

        client.SetStreamMode( ViconDataStream.Client.StreamMode.EClientPullPreFetch )
        print( 'Get Frame PreFetch', client.GetFrame(), client.GetFrameNumber() )

        client.SetStreamMode( ViconDataStream.Client.StreamMode.EServerPush )
        print( 'Get Frame Push', client.GetFrame(), client.GetFrameNumber() )

        print( 'Frame Rate', client.GetFrameRate() )

        try:
            client.SetApexDeviceFeedback( 'BogusDevice', True )
        except ViconDataStream.DataStreamException as e:
            print( 'No Apex Devices connected' )

        client.SetAxisMapping( ViconDataStream.Client.AxisMapping.EForward, 
                              ViconDataStream.Client.AxisMapping.ELeft, 
                              ViconDataStream.Client.AxisMapping.EUp )
        xAxis, yAxis, zAxis = client.GetAxisMapping()
        print( 'X Axis', xAxis, 'Y Axis', yAxis, 'Z Axis', zAxis )
        
        try:
            client.SetTimingLog( '', '' )
        except ViconDataStream.DataStreamException as e:
            print( 'Failed to set timing log' )

        try:
            client.ConfigureWireless()
        except ViconDataStream.DataStreamException as e:
            print( 'Failed to configure wireless', e )


        subjectNames = client.GetSubjectNames()
        for subjectName in subjectNames:
            segmentNames = client.GetSegmentNames( subjectName )
            for segmentName in segmentNames:
                segmentChildren = client.GetSegmentChildren( subjectName, segmentName )
                try:
                    print( segmentName, 'has static scale', 
                          client.GetSegmentStaticScale(subjectName
                                                       , segmentName))
                except ViconDataStream.DataStreamException as e:
                    print( 'Scale Error', e )               
                print( segmentName, 'has global translation', 
                      client.GetSegmentGlobalTranslation(subjectName,
                                                         segmentName))
                print( segmentName, 'has global rotation( helical )', 
                      client.GetSegmentGlobalRotationHelical(subjectName,
                                                             segmentName ) )               
                print( segmentName, 'has global rotation( EulerXYZ )', 
                      client.GetSegmentGlobalRotationEulerXYZ( subjectName,
                                                              segmentName ) )               
                print( segmentName, 'has global rotation( Quaternion )', 
                      client.GetSegmentGlobalRotationQuaternion( subjectName,
                                                                segmentName ) )               
                print( segmentName, 'has global rotation( Matrix )', 
                      client.GetSegmentGlobalRotationMatrix( subjectName,
                                                            segmentName ) )
                
                # TODO: Send this data to the PX4 autopilot 
                # software as a MAVLink Odometry message
                
            try:
                print( 'Object Quality', client.GetObjectQuality( subjectName ) )
            except ViconDataStream.DataStreamException as e:
                    print( 'Not present', e )

    except ViconDataStream.DataStreamException as e:
        print( 'Handled data stream error', e )

    print()

