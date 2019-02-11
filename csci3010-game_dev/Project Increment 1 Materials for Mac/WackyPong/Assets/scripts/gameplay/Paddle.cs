using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// This script used on the paddles
/// </summary>
public class Paddle : MonoBehaviour
{
	
	/// <summary>
	/// Use this for initialization
	/// </summary>
	void Start()
	{
        Rigidbody2D rb = gameObject.AddComponent(typeof(Rigidbody2D)) as Rigidbody2D;
    }
	
	/// <summary>
	/// Update is called once per frame
	/// </summary>
	void Update()
	{
		
	}
	
}
