let a = [
    "Distance between Two locations",
    "Coordinates are:",
    " Police Station: Longitude(26.2182) and Latitude(78.1770) ",
    "User Location: Longitude(26.25004) and Latitude( 78.1725) ",

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