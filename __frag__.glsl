


float dist2Line (vec2 p, vec2 segA,vec2 segB) {
	vec2 p2 = vec2(segB.x - segA.x,segB.y - segA.y);
	float num = p2.x * p2.x + p2.y * p2.y;
	float u = ((p.x - segA.x) * p2.x + (p.y - segA.y) * p2.y) / num;

	if (u > 1.0 ) {
		u = 1.0;
	}
	else if (u < 0.0) {
		u = 0.0;
	}

	float x = segA.x + u * p2.x;
	float y = segA.y + u * p2.y;

	float dx = x - p.x;
	float dy = y - p.y;

	return sqrt(dx*dx + dy*dy);
}



float DistToLine(vec2 pt1, vec2 pt2, vec2 testPt)
{
  vec2 lineDir = pt2 - pt1;
  vec2 perpDir = vec2(lineDir.y, -lineDir.x);
  vec2 dirToPt1 = pt1 - testPt;
  return abs(dot(normalize(perpDir), dirToPt1));
}

float nearestLine(in vec2 x) {
	int i,j=N-1;
	float dMin,d;
	dMin=32768.0;
	for (i=0;i<N;i++) {
		dMin=min(dMin,dist2Line( x,P[i] , P[j] ));
		//dMin=min(dMin,DistToLine( P[i] , P[j] , x ));
		j=i;
	}
	return dMin;
}


void main() {
	float v= nearestLine(gl_TexCoord[0].xy);
	v=sin(v);
	gl_FragColor= vec4(vec3(v),1.0);
}

