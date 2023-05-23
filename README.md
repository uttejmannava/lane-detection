# lane-detection

basically wanted to learn how FSD works and how cars can "see". 

learned a good chunk of OpenCV's repertoire and refreshed my knowledge of first-year linear algebra to understand how computers see pictures. learned that methods of distinguishing _things_ is simply noticing changes in pixel intensity. built on this to learn edge and contour detection, and moved into recognizing objects (by far one of the coolest parts of the process, I learned how those super-advanced-looking surveillance cameras in films draw squares around moving objects/people).

the algorithm works fairly well, however the parameters for the mask need to be changed depending on what angle the dashcam video is taken from, and how much of the vehicle's hood is visible in the frame. Additionally, parameters for detecting lines need to be updated according to lighting/time of day, since the upper and lower limits for how much a lane line needs to be visible to be actually detected depends on visibility. when fine tuned, the algorithm performs exceptionally well, especially for dashcam videos filmed on clear days.

next steps would be to work on object detection, the current method is crude since it looks for the absolute "difference" in subsequent frames (think of subtracting frames and seeing the changes). results in accidental detection of the changing lane lines themselves, or irrelevant background details. masking alone could not solve this issue. may need to result to OpenCV's ML functions to train with different datasets, to recognize cars, pedestrians, signs, etc.
