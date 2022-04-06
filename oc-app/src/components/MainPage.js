import React from 'react';

function MainPage () {
<<<<<<< HEAD
    const [VisStarted, setVisStarted] = useState(false)
    function HandleStartVis () {
        setVisStarted(!VisStarted)

        console.log(VisStarted)
    }
    
    if (VisStarted === false) {
=======
>>>>>>> parent of 9f5d92a (first version)
    return (
    <div className='Main'>
        <h1>
            Explore the OpenCitations dataset
        </h1>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque vulputate leo vel pulvinar maximus. Suspendisse rutrum dolor id lacus aliquet molestie. Mauris nec orci vel nisl blandit cursus ut non lacus. Phasellus eu libero purus. Curabitur hendrerit velit id eros lacinia, tincidunt finibus dui pretium. Duis tristique felis commodo quam porta faucibus. Aliquam ullamcorper urna vel ex elementum, id feugiat ipsum luctus. Praesent scelerisque varius mauris a tristique. Morbi congue ornare ante, posuere congue ligula placerat sit amet. Praesent posuere leo nisl, et molestie tellus pulvinar eget. Maecenas convallis neque ut lacus dignissim, in vestibulum urna consequat. Nulla facilisi. Phasellus non ex a magna dapibus luctus id ut velit. In at risus fringilla libero fringilla laoreet. Donec consectetur orci eu velit pretium, accumsan bibendum ligula consectetur. Vivamus aliquam vel risus sed malesuada.</p>
    </div>
    )};

export default MainPage;