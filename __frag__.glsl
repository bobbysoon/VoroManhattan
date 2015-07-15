




vec2 rand2(in vec2 p) {
	return fract(vec2(sin(p.x * 591.32 + p.y * 154.077), cos(p.x * 391.32 + p.y * 49.077)));
}


vec4 mod289(vec4 x) {
	return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec4 permute(vec4 x) {
	return mod289(((x*34.0)+1.0)*x);
}

vec4 taylorInvSqrt(vec4 r) {
	return 1.79284291400159 - 0.85373472095314 * r;
}

vec2 fade(vec2 t) {
	return t*t*t*(t*(t*6.0-15.0)+10.0);
}

// Classic Perlin noise
float cnoise(vec2 P) {
	vec4 Pi = floor(P.xyxy) + vec4(0.0, 0.0, 1.0, 1.0);
	vec4 Pf = fract(P.xyxy) - vec4(0.0, 0.0, 1.0, 1.0);
	Pi = mod289(Pi); // To avoid truncation effects in permutation
	vec4 ix = Pi.xzxz;
	vec4 iy = Pi.yyww;
	vec4 fx = Pf.xzxz;
	vec4 fy = Pf.yyww;

	vec4 i = permute(permute(ix) + iy);

	vec4 gx = fract(i * (1.0 / 41.0)) * 2.0 - 1.0 ;
	vec4 gy = abs(gx) - 0.5 ;
	vec4 tx = floor(gx + 0.5);
	gx = gx - tx;

	vec2 g00 = vec2(gx.x,gy.x);
	vec2 g10 = vec2(gx.y,gy.y);
	vec2 g01 = vec2(gx.z,gy.z);
	vec2 g11 = vec2(gx.w,gy.w);

	vec4 norm = taylorInvSqrt(vec4(dot(g00, g00), dot(g01, g01), dot(g10, g10), dot(g11, g11)));
	g00 *= norm.x;
	g01 *= norm.y;
	g10 *= norm.z;
	g11 *= norm.w;

	float n00 = dot(g00, vec2(fx.x, fy.x));
	float n10 = dot(g10, vec2(fx.y, fy.y));
	float n01 = dot(g01, vec2(fx.z, fy.z));
	float n11 = dot(g11, vec2(fx.w, fy.w));

	vec2 fade_xy = fade(Pf.xy);
	vec2 n_x = mix(vec2(n00, n01), vec2(n10, n11), fade_xy.x);
	float n_xy = mix(n_x.x, n_x.y, fade_xy.y);
	return 2.3 * n_xy;
}

float fbm(vec2 P, int octaves, float lacunarity, float gain) {
	float sum = 0.0;
	float amp = 1.0;
	vec2 pp = P;

	int i;

	for(i = 0; i < octaves; i+=1) {
		amp *= gain;
		sum += amp * cnoise(pp);
		pp *= lacunarity;
	}
	return sum;

}

float perlin(vec2 p, int octaves) {
	float l = 2.5;
	float g = 0.4;

	vec2 q = vec2( fbm( p + vec2(0.0,0.0),octaves,l,g),fbm( p + vec2(5.2,1.3),octaves,l,g));
	vec2 r = vec2( fbm( p + 4.0*q + vec2(1.7,9.2),octaves,l,g ), fbm( p + 4.0*q + vec2(8.3,2.8) ,octaves,l,g));
	return fbm( p + 4.0*r ,octaves,l,g);
}

float voronoi(in vec2 x, int iMax) {
	float val=1.0;
	x/=iMax;
	for (int iter=0;iter<iMax;iter++){
		vec2 p = floor(x);
		vec2 f = fract(x);
		float dxy=64.0;
		vec2 res = vec2(8);
		for(int j = -1; j <= 1; j ++) {
			for(int i = -1; i <= 1; i ++) {
				vec2 b = vec2(i, j);
				vec2 r = b - f + rand2(p + b);

				float d = mod(iter,2)==1 ? max(abs(r.x), abs(r.y)) : abs(r.x) + abs(r.y) ;

				if(d < res.x) {
					res.y = res.x;
					res.x = d;
				} else if(d < res.y)
					res.y = d;

				dxy = min(dxy,sqrt(res.x*res.x+res.y*res.y));
			}
		}
		val*= min(res.y-res.x,0.125)*8;
		val*= max(0.25,abs(cos(dxy)));
		//if (mod(iter,iMax)==iMax-1) val=max(val,perlin( x , 3));
		x/=.25;
	}
	return val;
}

float dist2Line (vec2 p, vec2 segA,vec2 segB) {
	vec2 p2 = vec2(segB.x - segA.x,segB.y - segA.y);
	float u = ((p.x - segA.x) * p2.x + (p.y - segA.y) * p2.y) / (p2.x * p2.x + p2.y * p2.y);

	if (u > 1.0 ) u = 1.0;
	else if (u < 0.0) u = 0.0;

	float dx = (segA.x + u * p2.x) - p.x;
	float dy = (segA.y + u * p2.y) - p.y;

	return sqrt(dx*dx + dy*dy);
}

int nearestLineIndex;
float nearestLine(in vec2 x) {
	int i,j=N-1;
	float dMin,d;
	nearestLineIndex=j;
	dMin=32768.0;
	for (i=0;i<N;i++) {
		d=dist2Line( x,P[i] , P[j] );
		dMin=min(dMin,d);
		if (dMin==d) nearestLineIndex=i;
		j=i;
	}
	return dMin;
}

#define TIME 0.0
#define pi 3.141593
void main() {
	float dist= nearestLine(gl_TexCoord[0].xy);
	float vor= voronoi(gl_TexCoord[0].xy , dist<pi?2:3);
	float val= dist<pi?pi-dist:min(sqrt(dist-pi),.125);
	val=min(val,vor);
	vec4 col= vec4(vec3(val),1.0);
	if (dist<pi) {
		float i=sin(pi-dist);
		col.x= i;
		col.y=min(i,col.y);
		col.z= i;
		//col.y*=1-(pi-dist);
	}
	gl_FragColor= col;
}

