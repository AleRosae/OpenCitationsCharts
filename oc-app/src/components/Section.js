import React, {useState} from 'react';
import { Link, DirectLink, Element, Events, animateScroll as scroll, scrollSpy, scroller } from 'react-scroll'
import MainPage from './MainPage';
import CreateDataVis from './DataVis';
import HomePage from "./HomePage";

const styles = {
  fontFamily: 'sans-serif',
  textAlign: 'center',
};
var MySect   = () => (pages.map(page => 
  <Element key = {"key_n"+page} className='sections' name={"Section"+page} >
      <CreateDataVis n_page={page} />
  </Element>))

const pages = [0, 1, 2, 3, 4]
function handleChange () {
    console.log("triggered");
    var MySect   = () => (pages.map(page => 
      <Element key = {"key_n"+page} className='sections' name={"Section"+page} >
          <CreateDataVis n_page={page} />
      </Element>))
        }

class Section extends React.Component {

  constructor(props) {
    super(props);
    this.scrollToTop = this.scrollToTop.bind(this);
  }

  componentDidMount() {

    Events.scrollEvent.register('begin', function () {
      console.log("begin", arguments);
    });

    Events.scrollEvent.register('end', function () {
      console.log("end", arguments);
      var MySect   = () => (pages.map(page => 
        <Element key = {"key_n"+page} className='sections' name={"Section"+page} >
            <CreateDataVis n_page={page} />
        </Element>))
        return (MySect)
    });

  }
  scrollToTop() {
    scroll.scrollToTop();
  }
  scrollTo() {
    scroller.scrollTo('scroll-to-element', {
      duration: 800,
      delay: 0,
      smooth: 'easeInOutQuart'
    })
  }
  scrollToWithContainer() {

    let goToContainer = new Promise((resolve, reject) => {

      Events.scrollEvent.register('end', () => {
        resolve();
        Events.scrollEvent.remove('end');
      });

      scroller.scrollTo('scroll-container', {
        duration: 800,
        delay: 0,
        smooth: 'easeInOutQuart'
      });

    });

    goToContainer.then(() =>
      scroller.scrollTo('scroll-container-second-element', {
        duration: 800,
        delay: 0,
        smooth: 'easeInOutQuart',
        containerId: 'scroll-container'
      }));
  }
  componentWillUnmount() {
    Events.scrollEvent.remove('begin');
    Events.scrollEvent.remove('end');
  }



  render() {


    return (
      <div>
  <nav className="navbar navbar-expand-md fixed-top navbar-light bg-light">
      <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul className="navbar-nav">
          <li key={"Main"} className='nav-item active'> <Link  activeClass="nav-item active" className="nav-link" to={"Main"} offset={-50}
                  spy={true} smooth={true} duration={1200} delay={150}>{"Home"}</Link></li>
          {pages.map(
              page =><li key={"li_"+page}>
                  <Link  onClick={handleChange} activeClass="nav-item active" className="nav-link" to={"Section"+page} offset={-50}
                  spy={true} smooth={true} duration={1000} delay={100}>{"Section"+page}</Link>
                  </li>
          )
          }
          </ul>
      </div>
  </nav>
          <HomePage />
          <div className="StartVis">
              <h2>Curios about what we have in our pockets?</h2>
          </div>

      <div>
         <MySect />
          
      </div>
</div>
          )  
        }
};

export default Section;

