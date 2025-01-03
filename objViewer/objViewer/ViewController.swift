import SceneKit
import Cocoa

class ViewController: NSViewController {
    var sceneView: SCNView!
    var scene: SCNScene!

    override func viewDidLoad() {
        super.viewDidLoad()

        for obj_name in obj_names {
            // Initialize the scene
            scene = SCNScene(named: "objs/02942699/\(obj_name)/models/model_normalized.obj")
            
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

let obj_names = ["b42c3da473bb4226dbe4bc54590e1d59", "483c387d6886e603314b44839465ec00", "b22e56fdf18e2eb8968b65a7871de463", "3b5838e660e2eee27f85a81aa54b70ae", "9726bf2b38d817eab169d2793795b997", "4700873107186c6e2203f435e9e6785", "d9bb9c5a48c3afbfb84553e864d84802", "3175f1c1d0cca3c6901887a0237c0ac2", "97cd28c085e3754f22c69c86438afd28", "9d79c246317bbbe87f72d6c7f2024896", "935fc76352a4d5fd72a90fe1ba02202a", "82819e1201d2dc583a3e53900c6cbba", "fd058128095abf343ce579773d34f5bf", "c9c9ffd08af8b268b52759c2c2fc0d1e", "ce40b134b11e8c822bbc2c380e91dfe2", "7e677756898b40dc39513d756da531d0", "2693df58698a2ca29c723bc28575d785", "a4b0c73d0f12bc75533388d244d29c5c", "d5624d29159a4cdb7e1c85c5c15da7fb", "936a458fdb8eb12171dc2053392a6e6f", "74ebdf5a3cdf33ebc6966f67e1bb9e90", "97690c4db20227d248e23e2c398d8046", "60923e8a6c785a8755a834a7aafb0236", "2fc6168fba3ef6953ada8db96f6d95a3", "6ed69b00b4632b6e07718ee10b83e10", "7077395b60bf4aeb3cb44973ec1ffcf8", "9db4b2c19c858a36eb34db531a289b8e", "e9f2c58d90e723f7cc57882dfaef8a57", "39419e462f08dcbdc98cccf0d0f53d7", "6ca77b19e3f52c5031c1d3ccd72d7161", "3d18881b51009a7a8ff43d2d38ae15e1", "68f66f5ab594fd3cc2890daf3a9f7413", "f7e2afd70e37f60ad2b6f4e920e50f96", "d680d61f934eaa163b211460f022e3d9", "317a7ea24e661ce3bfc146552c7aa5d2", "c802792f388650428341191174307890", "416ce9adf7ad40f4959c1c3d740c4f1", "a3c9dcaada9e04d09061da204e7c463c", "eb86c8c2a20066d0fb1468f5fc754e02", "9cdaf68ed1e1daba9c21adf7cd249be9", "1298634053ad50d36d07c55cf995503e", "5334cfe15f80099f15ac67104577aee7", "4f2a9bf0d8eb00e0a570c6c691c987a8", "fe669947912103aede650492e45fb14f", "58e9faa223142b7fd5af42f3e1f05e3f", "98fc1afc8dec9773b10c2418bc64b141", "509017601d92a7d1db286a46dfc37518", "e85debbd554525d198494085d68ad6a0", "5d42d432ec71bfa1d5004b533b242ce6", "89f0e0da4747aad1172ac9cfeff21994", "1ab3abb5c090d9b68e940c4e64a94e1e", "15e72ce7a8a328d1fd9cfa6c7f5305bc", "cef23409b1a030d516fe5320f9715eef", "cd5fd9a2bd6792ad318e2f26ee2da02c", "73b02fe7b4b2e45f74cd541b34c6124", "ff74c4d2e710df3401a67448bf8fe08", "a59cbd50ecf38a1be2dc67b821479cc4", "4cd861035c740db5a33f3afcb8763f26", "3019eea689e5d9c1fb045022c5d3b1e2", "4852ee95e7bd8556c60396a717ba6c7e", "fdcd83539b8db2c8b5635bf39f10a28a", "d6721b4ee3d004b8c7e03242f1bf8d19", "45b01c604426a0a9c5c10e0ebb47766c", "657a650215e453846f90fff80f29e77d", "a230560372fd55a410ec06105f027b7d", "3b56239e45828d2bb4521a835b1946c8", "87b8cec4d55b5f2d75d556067d060edf", "22217d5660444eeeca93934e5f39869", "b42c73b391e14cb16f05a1f780f1cef", "3d81cebaa1226e9329fdbaf17f41d872", "cda4fc24b2a602b5b5328fde615e4a0c", "90198c0aaf0156ce764e2db342c0e628", "2c0b4e318766e01723cd81bf29b64a1", "2153bc743019671ae60635d9e388f801", "db663e3f7ee9869f5c351e299b24e355", "8b4f63046ee3bf99373b92b376321e13", "51176ec8f251800165a1ced01089a2d6", "290abe056b205c08240c46d333a693f", "7ef29f8a7a132c46e0afa7d1aded497", "6c14c6f6cca53a6710d0920f7087353b", "fb3b5fae94f7b02a3b269928487f8a4c", "63c10cfd6f0ce09a241d076ab53023c1", "c3e6564fe7c8157ecedd967f62b864ab", "17a010f0ade4d1fd83a3e53900c6cbba", "147183af1ba4e97b8a94168388287ad5", "9533618250e35304514fae39ba03db5", "e9e22de9e4c3c3c92a60bd875e075589", "a600991b042b2d5492348cc032adf089", "c3a410e532cbf900e5a8b3dc188dc518", "9e91f482b829c4d1e9fff7dfdebc774b", "e57aa404a000df88d5d4532c6bb4bd2b", "6d036fd1c70e5a5849493d905c02fa86", "b27815a2bde54ad3ab3dfa44f5fab01", "5265ff657b9db80cafae29a76344a143", "d1a3482c576f8c50592ecd319dfd8c5d", "ee0f44a37e50eda2a39b1d7ef8834b0", "a8961c59576972cb57682b709eb0ab19", "a9408583f2c4d6acad8a06dbee1d115", "1967344f80da29618d342172201b8d8c", "ee58b922bd93d01be4f112f1b3124b84", "e3dc17dbde3087491a722bdf095986a4", "550aea46c75351a387cfe978d99ba05d", "77096e9094680faf603e5a6a09a35395", "235a6dd25c0a6f7b66f19f26ac490096", "21f65f53f74f1b58de8982fc28ddacc3", "1cc93f96ad5e16a85d3f270c1c35f1c7", "f1540b3d6da38fbf1d908355fc20d631", "e67273eff31fabce656c3a28e34d04c4", "46c09085e451de8fc3c192db90697d8c", "ec28a64bdf9501161bfbba8a5defb02", "fc83047701a0e21b901ee6249a8d9beb", "b92acfcd92408529d863a5ae2bdfd29", "9b4953f653bfdd40ea41ceac179ca4d4"]
