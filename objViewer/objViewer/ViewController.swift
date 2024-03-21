import SceneKit
import Cocoa

class ViewController: NSViewController {
    var sceneView: SCNView!
    var scene: SCNScene!

    override func viewDidLoad() {
        super.viewDidLoad()

        for obj_name in obj_names {
            // Initialize the scene
            scene = SCNScene(named: "objs/03513137/\(obj_name)/models/model_normalized.obj")
            
            // Setup the scene view
            sceneView = SCNView(frame: NSRect(origin: self.view.bounds.origin, size: CGSize(width: self.view.bounds.height, height: self.view.bounds.height)))
            sceneView.scene = scene
            self.view.addSubview(sceneView)
            
            // Add camera
            let cameraNode = SCNNode()
            cameraNode.camera = SCNCamera()
            cameraNode.position = SCNVector3(x: 0, y: 0, z: 0)
            scene.rootNode.addChildNode(cameraNode)
            sceneView.pointOfView = cameraNode
            
            // Add light
            let lightNode = SCNNode()
            lightNode.light = SCNLight()
            lightNode.light!.type = .omni
            lightNode.position = SCNVector3(x: 0, y: 20, z: -20)
            scene.rootNode.addChildNode(lightNode)
            
            // Add an ambient light
            let ambientLightNode = SCNNode()
            ambientLightNode.light = SCNLight()
            ambientLightNode.light!.type = .ambient
            ambientLightNode.light!.color = NSColor.darkGray
            scene.rootNode.addChildNode(ambientLightNode)
            
            // Rotate and take screenshots
            takeScreenshotsAroundObject(obj_name, cameraNode, sceneView)
        }
    }
    
    func takeScreenshotsAroundObject(_ obj_name: String, _ cameraNode: SCNNode, _ sceneView: SCNView) {
        let steps = [0, 30.0 / 90.0 * .pi/2, 75.0 / 90.0 * .pi/2]
        let radius: Float = 1.5

        for (step, angle) in steps.enumerated() {
            // Calculate the angle in radians
            let angle = -.pi / 2 + angle
            
            // Calculate the new camera position
            let x = radius * cos(Float(angle))
            let z = radius * sin(Float(angle))
            cameraNode.position = SCNVector3(x, Float(cameraNode.position.y), z)
            
            print(cameraNode.position)
            
            // Ensure the camera is always looking at the center of the scene
            let lookAtCenter = SCNLookAtConstraint(target: scene.rootNode)
            cameraNode.constraints = [lookAtCenter]
            
            // Wait for the scene to update
            let screenshot = sceneView.snapshot()
            self.saveImage(screenshot, withName: "\(obj_name)_\(step + 1)")
        }
    }
    
    func saveImage(_ image: NSImage, withName name: String) {
        guard let data = image.tiffRepresentation,
              let bitmapImage = NSBitmapImageRep(data: data),
              let imageData = bitmapImage.representation(using: .png, properties: [:]) else { return }
        
        let fileURL = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!.appendingPathComponent("\(name).png")
        
        do {
            try imageData.write(to: fileURL)
            print("Saved image to \(fileURL.path)")
        } catch {
            print("Error saving image: \(error)")
        }
    }
}

let obj_names = ["48b7dafda49b9175365930cae725a1a", "5f0fab98fec5f53bfac6099f3d4830fe", "f778971235a67bba754cd8e5dd1ab945", "8f17e31867f1968969b2407ca5e1a9ac", "fd861e0998b5acddb20f6e48f6a30cbf", "96366015f183b237f1ea818b22320c8b", "be9b9c3bd70c6f5c785b8fa1ee371fb3", "65bd772022c2ac094fd7d35b0d9ebb77", "bab3a20dee03a0f0e4773d7a183337d9", "6fea034555e60897e9fed33f81b1fa79", "3aad2f60419948f891003fe635f8d594", "d739548a9b15c18cfac6099f3d4830fe", "6429cf540f58c246226eabe1cca3e850", "adf9b0eaf3a1980187710597b0363fe6", "68106146958b708540b769487f41c4b", "dc10f3b2b8cf3c8f3a0407ebaf7dd3a5", "8d50220bdf7be7b92d356a2793fb4d69", "21d201f43ddd36c52fafb0cab311e6a", "17969fc40964dbe0288d8f1144f7979f", "257676761b471e0e69508b2b14833df3", "50c322394e1587c54e5e6ac3ef6bff73", "a452a0857cb46b5226eabe1cca3e850", "d736c45c5b2397219092826e64279378", "737e1c921100f038e263fa6049be3541", "a50fdcc3128ca95c663e90eaf6b4ca52", "190364ca5d1009a324a420043b69c13e", "cd7ecd4007cf6738807322bc19906e74", "bb3a039ef88a9fbc480514d7f2edc0a3", "d25312c53aa9ded3b57cb9238c4c8e81", "2171c3694013b15177b4e19e75551fd3", "9cdf5e674bf943bf69ed2daa3338779", "1cebc02c679add362f20449572a3a77c", "c354dab2bcbe9c68d6d40d1978baee1c", "a8e04b323931f2b9f2c6c460ab16f409", "5021db37ba1fb177202339ec5396045d", "c3fb3e4f87ca6c91388f6c7a9d3e1552", "c347db0e6df5e11efbf020c099468179", "a1bf8b293de641b5a5cc2b36a8952e0d", "73b749a0704ad08398ce5d19cf9bd7c9", "1d1cc96025786db595f577622f465c85", "27e52dac4cafdfee2a04c68bc263be", "7721ee80bfa4cbc583ce6bc80d855733", "8b6b50321f5d5ba114300f3e8908fff", "a1357ff99c759de448d4a59eba9f268c", "20ba624db264002082ee371ba207c717", "802b08904ed6bb57b20f6e48f6a30cbf", "fbe830888a111027b20f6e48f6a30cbf", "7a0772798520e9e141bb12648ac801b9", "9668f0abd848e943b20f6e48f6a30cbf", "73359cd0e38579745c351e299b24e355", "ecabb65ac86924cfea1118e44682a5ab", "43f6f91a2a64a62b5fd0ea7ae0dec99c", "1ae94e883149a07a242154514ef1967f", "13da2cd827cc8b9f99976ddcaae4d11", "10dee7587a785cbfe22dbe8dd678fde8", "ae0a3cf547c0534ab0aa56928723eca5", "89815c92980efb27226eabe1cca3e850", "272cd30169e040d3aac6013f3e2b09f9", "eeaf3811af59e557cdc59d2b768bcb80", "f2513143d0467e357af69fbb2f9a628a", "bde25e25b138b1f75d21ec234969aa2c", "179b3b1df301b95ccc34b900bb2492e", "7f8767aac7a5bbefef6f32a2a0bd4e8f", "77266730e34800638d23b8b99c98bb6e", "aa51f885208208375094ac652b5174eb", "f04ce9786ba0364b6e686498ed562f91", "d516787b65d08365480514d7f2edc0a3", "6f41517d1eec863b52fafb0cab311e6a", "ae8a2ae90ac11bd93d4e343a1ac21b93", "ee4046b8154cf9fd5964bcdfbf477f81", "8eb4152bc0f6b91e7bc12ebbbb3689a1", "b3049575684f6ebfc0e57505cc92501b", "59c1f0cc533e57a7d44412b02a9868", "7f03445e003b692f3fd0acbaa54efdfa", "f232d07e98fae2d4eeb425ad8cf9eedc", "eafb1b2b77dbf8c8172c0c1bc4c72a8c", "3621cf047be0d1ae52fafb0cab311e6a", "b166d9115ed7b7638e75bb5638d14ce9", "a6d6d755b17fdbbc3e8b63b9578c7894", "f59e8dac9451d165a68447d7f5a7ee42", "d76f5069b5f42903b20f6e48f6a30cbf", "176bb6178d49f5ace01c07526cf2aa4", "30c9fc79edc88adf438fdee28ab485d3", "a612b83619ce985f3de9dfa8d65133cb", "43c7b9475c17df536b9e4b1418714282", "5174613439e9cf79d2808af04871028b", "2a6f4a2ff5e11b264dead5f22c05efdf", "3497a6217d54da094dd343ea1de55435", "82e027e4b43fa602f99976ddcaae4d11", "aba5ab07cb21bf4454631ce860fd196c", "93a86f07803b31c7715a42c4b7cc3a54", "cdbefa5bb13ada4a52fafb0cab311e6a", "b14fa79d2a1efb586f7dd5dd40daa88a", "69d70c404f47b1f9b137667443c4be42", "791c70769828cda852bc033e87de1006", "77cdfb9d433531c6a8963fe61f2bc75f", "dde4e367492ca88bce01c07526cf2aa4", "69ece333c6d386ebbeee9a165d0dbe2", "4f0ae9814adde64f6a12484fa9d9be10", "956fc471237a3e55613792009f64ab4d", "608f7c4d52bbfeec9f00d9b3defbf21d", "57ffd28975abba38480514d7f2edc0a3", "d7a860627e8ba083ec3df6ee3b84fcd3", "20ef9affd966bb53727b087f26084eb", "d8b02a2ef9de06702e85eab6bca44d5c", "cfd3bb444cb730458636fc327bbb2619", "12a5eb233ecf486e3e01acc90dd935ff", "3b45ee42f62559c74e5e6ac3ef6bff73", "7c3bf8abf7b2b41e172c0c1bc4c72a8c", "f0a1e3c919471b2819fa27f3bdd7d71c", "93acbfac563ebc4c1d05dd90478fa7ec", "51ee565cc330e131b20f6e48f6a30cbf", "22ff6fc2c81a3674823590ed8a67d74b", "e3d98ac62469795b20f6e48f6a30cbf", "be9812128882a7957e167bb4cf1b28cc", "ba62b73074d51637b61d7759f8544b8a", "32396b24a2106049a8963fe61f2bc75f", "b4c223db8b1a30016cf94eaa382e4d1", "e143d40f9df57d92288d8f1144f7979f", "854adc84a21c0a1de8fe5a1391785bf6", "1f3aa976ccfc9e66780b70108bbf4c51", "e0b4672fbbae71a49617e37e5a669a71", "6e082b8d5dfe38c0c4278fc12d4f4d35", "8018b307a127ec8d4051b6e037481c7", "3e3e8a71c208d991226eabe1cca3e850", "9cbcaecc65c3a511eeb5508ef773ccb1", "8e624ace735e6baf96c3bfb1b184602c", "8942f437af8771afa1702a37604ec6f", "587ff99119fe5c0efac6099f3d4830fe", "709348783d9c30c970290a7176ca24df", "ddc07c47962fe10f61f42fcc6613af2d", "92c11ff47a2d1a4f673a614c45f3afe4", "e176a78b82a5add0de8982fc28ddacc3", "8322568841b84054b581f592cbd3b472", "2750a9be8f6cbce54e5e6ac3ef6bff73", "f2107d6768adf4952fafb0cab311e6a", "9c5d16afab1cd899d1f50c75142faa8a", "2aaea503ebc42ddfdfc54a7d3e3d4e77", "d8736fc5b77ac6d26e686498ed562f91", "7da461d2b7ac1454e5e6ac3ef6bff73", "45d6e3b0b91073af7359b134afde902", "37f55552b517eceb501db4f27570eeec", "385480a2554374862cc4218c4be3f082", "6ff1a99371f10144e5e6ac3ef6bff73", "500502549d46f6d34e61e54863a9d5af", "e4ac62dd8caeabb1f80d3a620e00dd9a", "58fe8b9f7026cd2bf1c20b7f59bbc099", "3a12b9c4f7f08b8efac6099f3d4830fe", "354b570e62b161b8b20f6e48f6a30cbf", "13f607a462bd1ea83b13741399690655", "1dc0db78671ac363f99976ddcaae4d11", "96e81d71a15ecb1dd3f1ead878957615", "7e4e3a4a38a589232f20449572a3a77c", "64010c4042824e03b13741399690655", "dfc0f60a1b11ab7c388f6c7a9d3e1552", "c54fc7db01647d02823590ed8a67d74b", "366a517ee3a9aa3db4c1516b11b344e0", "91c0193d38f0c5338c9affdacaf55648", "4730ce6da5433f3bd93d030573255054", "2c9086096c0fe9889215d30ce83ed4dd", "fe47f10f637b54594e5e6ac3ef6bff73", "777497c94098014818457223b2b684b3"]

// paths for cameras (02942699)
// let obj_names = ["b42c3da473bb4226dbe4bc54590e1d59", "483c387d6886e603314b44839465ec00", "b22e56fdf18e2eb8968b65a7871de463", "3b5838e660e2eee27f85a81aa54b70ae", "9726bf2b38d817eab169d2793795b997", "4700873107186c6e2203f435e9e6785", "d9bb9c5a48c3afbfb84553e864d84802", "3175f1c1d0cca3c6901887a0237c0ac2", "97cd28c085e3754f22c69c86438afd28", "9d79c246317bbbe87f72d6c7f2024896", "935fc76352a4d5fd72a90fe1ba02202a", "82819e1201d2dc583a3e53900c6cbba", "fd058128095abf343ce579773d34f5bf", "c9c9ffd08af8b268b52759c2c2fc0d1e", "ce40b134b11e8c822bbc2c380e91dfe2", "7e677756898b40dc39513d756da531d0", "2693df58698a2ca29c723bc28575d785", "a4b0c73d0f12bc75533388d244d29c5c", "d5624d29159a4cdb7e1c85c5c15da7fb", "936a458fdb8eb12171dc2053392a6e6f", "74ebdf5a3cdf33ebc6966f67e1bb9e90", "97690c4db20227d248e23e2c398d8046", "60923e8a6c785a8755a834a7aafb0236", "2fc6168fba3ef6953ada8db96f6d95a3", "6ed69b00b4632b6e07718ee10b83e10", "7077395b60bf4aeb3cb44973ec1ffcf8", "9db4b2c19c858a36eb34db531a289b8e", "e9f2c58d90e723f7cc57882dfaef8a57", "39419e462f08dcbdc98cccf0d0f53d7", "6ca77b19e3f52c5031c1d3ccd72d7161", "3d18881b51009a7a8ff43d2d38ae15e1", "68f66f5ab594fd3cc2890daf3a9f7413", "f7e2afd70e37f60ad2b6f4e920e50f96", "d680d61f934eaa163b211460f022e3d9", "317a7ea24e661ce3bfc146552c7aa5d2", "c802792f388650428341191174307890", "416ce9adf7ad40f4959c1c3d740c4f1", "a3c9dcaada9e04d09061da204e7c463c", "eb86c8c2a20066d0fb1468f5fc754e02", "9cdaf68ed1e1daba9c21adf7cd249be9", "1298634053ad50d36d07c55cf995503e", "5334cfe15f80099f15ac67104577aee7", "4f2a9bf0d8eb00e0a570c6c691c987a8", "fe669947912103aede650492e45fb14f", "58e9faa223142b7fd5af42f3e1f05e3f", "98fc1afc8dec9773b10c2418bc64b141", "509017601d92a7d1db286a46dfc37518", "e85debbd554525d198494085d68ad6a0", "5d42d432ec71bfa1d5004b533b242ce6", "89f0e0da4747aad1172ac9cfeff21994", "1ab3abb5c090d9b68e940c4e64a94e1e", "15e72ce7a8a328d1fd9cfa6c7f5305bc", "cef23409b1a030d516fe5320f9715eef", "cd5fd9a2bd6792ad318e2f26ee2da02c", "73b02fe7b4b2e45f74cd541b34c6124", "ff74c4d2e710df3401a67448bf8fe08", "a59cbd50ecf38a1be2dc67b821479cc4", "4cd861035c740db5a33f3afcb8763f26", "3019eea689e5d9c1fb045022c5d3b1e2", "4852ee95e7bd8556c60396a717ba6c7e", "fdcd83539b8db2c8b5635bf39f10a28a", "d6721b4ee3d004b8c7e03242f1bf8d19", "45b01c604426a0a9c5c10e0ebb47766c", "657a650215e453846f90fff80f29e77d", "a230560372fd55a410ec06105f027b7d", "3b56239e45828d2bb4521a835b1946c8", "87b8cec4d55b5f2d75d556067d060edf", "22217d5660444eeeca93934e5f39869", "b42c73b391e14cb16f05a1f780f1cef", "3d81cebaa1226e9329fdbaf17f41d872", "cda4fc24b2a602b5b5328fde615e4a0c", "90198c0aaf0156ce764e2db342c0e628", "2c0b4e318766e01723cd81bf29b64a1", "2153bc743019671ae60635d9e388f801", "db663e3f7ee9869f5c351e299b24e355", "8b4f63046ee3bf99373b92b376321e13", "51176ec8f251800165a1ced01089a2d6", "290abe056b205c08240c46d333a693f", "7ef29f8a7a132c46e0afa7d1aded497", "6c14c6f6cca53a6710d0920f7087353b", "fb3b5fae94f7b02a3b269928487f8a4c", "63c10cfd6f0ce09a241d076ab53023c1", "c3e6564fe7c8157ecedd967f62b864ab", "17a010f0ade4d1fd83a3e53900c6cbba", "147183af1ba4e97b8a94168388287ad5", "9533618250e35304514fae39ba03db5", "e9e22de9e4c3c3c92a60bd875e075589", "a600991b042b2d5492348cc032adf089", "c3a410e532cbf900e5a8b3dc188dc518", "9e91f482b829c4d1e9fff7dfdebc774b", "e57aa404a000df88d5d4532c6bb4bd2b", "6d036fd1c70e5a5849493d905c02fa86", "b27815a2bde54ad3ab3dfa44f5fab01", "5265ff657b9db80cafae29a76344a143", "d1a3482c576f8c50592ecd319dfd8c5d", "ee0f44a37e50eda2a39b1d7ef8834b0", "a8961c59576972cb57682b709eb0ab19", "a9408583f2c4d6acad8a06dbee1d115", "1967344f80da29618d342172201b8d8c", "ee58b922bd93d01be4f112f1b3124b84", "e3dc17dbde3087491a722bdf095986a4", "550aea46c75351a387cfe978d99ba05d", "77096e9094680faf603e5a6a09a35395", "235a6dd25c0a6f7b66f19f26ac490096", "21f65f53f74f1b58de8982fc28ddacc3", "1cc93f96ad5e16a85d3f270c1c35f1c7", "f1540b3d6da38fbf1d908355fc20d631", "e67273eff31fabce656c3a28e34d04c4", "46c09085e451de8fc3c192db90697d8c", "ec28a64bdf9501161bfbba8a5defb02", "fc83047701a0e21b901ee6249a8d9beb", "b92acfcd92408529d863a5ae2bdfd29", "9b4953f653bfdd40ea41ceac179ca4d4"]
