let a = [
    "Initializing user location....",
    "Fetching the API of the user..",
    "Trying to connect with camera...",
    "Error occured..",
    "Again Fetching ...",
    "Premission Access...",
    "Access Camera",
    "Request access to the camera..",
    "Displaying the video stream in the video element...",
    "Location Fetched...",
    ]
    const sleep = async(seconds)=>{
        return new Promise((resolve,reject)=>{
            setTimeout(()=>{
                resolve(true)
            }, seconds*1000)
        })
    }
    const locafetching = async(message)=>{
        await sleep(2)
        console.log(message)
    }
    (async()=>{
        for(let i = 0; i<a.length;i++){
            await locafetching(a[i])
        }
    })()